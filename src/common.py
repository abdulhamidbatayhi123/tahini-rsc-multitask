"""Shared data, preprocessing, models and metrics for the RSC Advances multitask study.

Every choice here follows DESIGN.md (fixed before any grouped result was computed)."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import os as _os
torch.set_num_threads(int(_os.environ.get("TORCH_THREADS", torch.get_num_threads())))
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

ROOT = Path(__file__).resolve().parents[1]
DATA_XLSX = ROOT / "source_repo" / "data" / "tahini" / "Tahin_Aycicek1.xlsx"
CACHE = ROOT / "audit" / "tahini.pkl"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

META = ["isim", "Tağşiş Var mı", "Tahin Oranı", "Ayçiçek ezmesi oranı", "Fıstık Ezmesi Oranı"]
COMP = ["tahini", "sunflower", "peanut"]
CHEM_REGIONS = [(600.0, 1800.0), (2800.0, 3050.0)]   # DESIGN.md primary input
torch.set_num_threads(max(1, (os.cpu_count() or 2) // 2))


def sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load():
    """Return dict with X (n, p) ascending wavenumber, wn, y (n,3) fractions in % [tahini, sunflower,
    peanut], tag (n,), group (n,), lot (n,)."""
    if CACHE.exists():
        df = pd.read_pickle(CACHE)
    else:
        df = pd.read_excel(DATA_XLSX)
        df.to_pickle(CACHE)
    wcols = [c for c in df.columns if c not in META]
    wn = np.array([float(str(c).replace(",", ".")) for c in wcols])   # headers use decimal commas
    order = np.argsort(wn)
    X = df[wcols].to_numpy(float)[:, order]
    wn = wn[order]
    y = df[["Tahin Oranı", "Ayçiçek ezmesi oranı", "Fıstık Ezmesi Oranı"]].to_numpy(float)
    assert np.allclose(y.sum(1), 100.0)
    g = df["isim"].astype(str).to_numpy()
    tag = df["Tağşiş Var mı"].astype(int).to_numpy()
    assert np.array_equal(tag, (y[:, 0] < 100).astype(int))
    lot = np.array([s.split("_")[0] for s in g])
    return dict(X=X, wn=wn, y=y, tag=tag, group=g, lot=lot)


def snv(X):
    return (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)


def region_mask(wn, regions=CHEM_REGIONS):
    m = np.zeros_like(wn, bool)
    for lo, hi in regions:
        m |= (wn >= lo) & (wn <= hi)
    return m


def features(d, regions="chem"):
    """SNV over the full spectrum, then keep the chosen regions (SNV is per spectrum: no leakage)."""
    if regions == "chemsnv":     # sensitivity (referee read 2026-11-10): SNV over the retained regions only
        m = region_mask(d["wn"])
        return snv(d["X"][:, m]), d["wn"][m]
    if regions == "chem700":     # sensitivity: ZnSe low-wavenumber edge excluded (fingerprint 700-1800)
        Z = snv(d["X"])
        m = region_mask(d["wn"], [(700.0, 1800.0), (2800.0, 3050.0)])
        return Z[:, m], d["wn"][m]
    Z = snv(d["X"])
    if regions == "full":
        return Z, d["wn"]
    m = region_mask(d["wn"])
    return Z[:, m], d["wn"][m]


def primary_split(d):
    """Foods grouped 70/30 hold-out (kanfood.split.group_holdout_split, seed 42)."""
    gss = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=42)
    return next(gss.split(np.zeros(len(d["group"])), groups=d["group"]))


def lolo_folds(d):
    return [(L, np.where(d["lot"] != L)[0], np.where(d["lot"] == L)[0]) for L in sorted(set(d["lot"]))]


# ------------------------------------------------------------------------------------------ PLS
def _pls_fit(X, Y, k):
    m = PLSRegression(n_components=k, scale=False)
    m.fit(X, Y)
    return m


def comp_from_pls(P):
    """Clip negative fractions at 0 and rescale to 100 %."""
    P = np.clip(P, 0, None)
    s = P.sum(1, keepdims=True)
    s[s == 0] = 1
    return 100 * P / s


def select_pls_k(X, Y, groups, kmax=25, score="rmse"):
    """Number of components by grouped 5-fold CV (minimum RMSECV of Y) inside the training set."""
    gkf = GroupKFold(n_splits=5)
    errs = np.zeros(kmax)
    for tr, va in gkf.split(X, Y, groups):
        for k in range(1, kmax + 1):
            m = _pls_fit(X[tr], Y[tr], k)
            errs[k - 1] += ((m.predict(X[va]) - Y[va]) ** 2).sum()
    return int(np.argmin(errs) + 1), errs


class PLSPair:
    """PLS-DA (PLS2 on one-hot class) + PLS regression on the three fractions."""

    def fit(self, X, y, tag, groups):
        self.kr, _ = select_pls_k(X, y, groups)
        self.reg = _pls_fit(X, y, self.kr)
        Yc = np.c_[1 - tag, tag].astype(float)
        self.kc, _ = select_pls_k(X, Yc, groups)
        self.cls = _pls_fit(X, Yc, self.kc)
        return self

    def predict(self, X):
        comp = comp_from_pls(self.reg.predict(X))
        s = self.cls.predict(X)
        score = s[:, 1] - s[:, 0]            # >0 means class "adulterated" (argmax of PLS-DA)
        return dict(comp=comp, score=score, prob=None, decide=(score > 0).astype(int))


# --------------------------------------------------------------------------------------- MT-DNN
class MTNet(torch.nn.Module):
    def __init__(self, p):
        super().__init__()
        self.body = torch.nn.Sequential(torch.nn.Linear(p, 128), torch.nn.ReLU(), torch.nn.Dropout(0.2),
                                        torch.nn.Linear(128, 64), torch.nn.ReLU())
        self.cls = torch.nn.Linear(64, 1)
        self.reg = torch.nn.Linear(64, 3)

    def forward(self, x):
        h = self.body(x)
        return self.cls(h).squeeze(-1), torch.softmax(self.reg(h), -1)


class MTDNN:
    """Multitask DNN of DESIGN.md: early stopping on a grouped inner validation split chooses the number of
    epochs; with refit=True (amendment A2) the network is then retrained from scratch on ALL training
    samples for that number of epochs, so that no training sample (or authentic lot) is left out."""

    def __init__(self, seed=0, max_epochs=300, patience=30, w=10.0, lr=1e-3, batch=32, min_epochs=20,
                 smooth=0.05, wd=1e-4, refit=True):
        self.seed, self.max_epochs, self.patience, self.w, self.lr, self.batch = seed, max_epochs, patience, w, lr, batch
        self.min_epochs, self.smooth, self.wd, self.refit = min_epochs, smooth, wd, refit

    def _train_full(self, X, y, tag, n_epochs):
        """Retrain from scratch on all given samples for n_epochs (same seed, same optimiser settings)."""
        rng = np.random.RandomState(self.seed)
        torch.manual_seed(self.seed)
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-8
        Xt = torch.tensor((X - self.mu) / self.sd, dtype=torch.float32)
        Tt = torch.tensor(tag, dtype=torch.float32)
        Yt = torch.tensor(y / 100, dtype=torch.float32)
        net = MTNet(X.shape[1])
        opt = torch.optim.Adam(net.parameters(), lr=self.lr, weight_decay=self.wd)
        for _ in range(n_epochs):
            net.train()
            perm = rng.permutation(len(Xt))
            for i in range(0, len(perm), self.batch):
                b = perm[i:i + self.batch]
                loss, _, _ = self._loss(net, Xt[b], Tt[b], Yt[b])
                opt.zero_grad()
                loss.backward()
                opt.step()
        net.eval()
        return net

    def _loss(self, net, xb, tb, yb):
        logit, comp = net(xb)
        tb = tb * (1 - self.smooth) + 0.5 * self.smooth          # label smoothing (amendment A1)
        bce = torch.nn.functional.binary_cross_entropy_with_logits(logit, tb)
        mse = ((comp - yb) ** 2).mean()
        return bce + self.w * mse, bce, mse

    def fit(self, X, y, tag, groups, val_groups_frac=0.2):
        rng = np.random.RandomState(self.seed)
        torch.manual_seed(self.seed)
        gss = GroupShuffleSplit(n_splits=1, test_size=val_groups_frac, random_state=self.seed)
        tr, va = next(gss.split(X, groups=groups))
        self.mu, self.sd = X[tr].mean(0), X[tr].std(0) + 1e-8
        f = lambda A: torch.tensor((A - self.mu) / self.sd, dtype=torch.float32)
        Xt, Xv = f(X[tr]), f(X[va])
        Tt, Tv = torch.tensor(tag[tr], dtype=torch.float32), torch.tensor(tag[va], dtype=torch.float32)
        Yt, Yv = torch.tensor(y[tr] / 100, dtype=torch.float32), torch.tensor(y[va] / 100, dtype=torch.float32)
        net = MTNet(X.shape[1])
        opt = torch.optim.Adam(net.parameters(), lr=self.lr, weight_decay=self.wd)
        best, best_state, wait, hist = np.inf, None, 0, []
        for ep in range(self.max_epochs):
            net.train()
            perm = rng.permutation(len(Xt))
            tl = []
            for i in range(0, len(perm), self.batch):
                b = perm[i:i + self.batch]
                loss, _, _ = self._loss(net, Xt[b], Tt[b], Yt[b])
                opt.zero_grad()
                loss.backward()
                opt.step()
                tl.append(loss.item() * len(b))
            net.eval()
            with torch.no_grad():
                vl, vb, vm = (v.item() for v in self._loss(net, Xv, Tv, Yv))
            hist.append(dict(epoch=ep + 1, train=sum(tl) / len(Xt), val=vl, val_bce=vb, val_mse=vm))
            if ep + 1 >= self.min_epochs and vl < best - 1e-6:
                best, wait = vl, 0
                best_state = {k: v.clone() for k, v in net.state_dict().items()}
                self.best_epoch = ep + 1
            elif ep + 1 >= self.min_epochs:
                wait += 1
                if wait >= self.patience:
                    break
        net.load_state_dict(best_state)
        self.net, self.history = net, pd.DataFrame(hist)
        if self.refit:
            self.net = self._train_full(X, y, tag, self.best_epoch)
        return self

    def predict(self, X):
        self.net.eval()
        with torch.no_grad():
            logit, comp = self.net(torch.tensor((X - self.mu) / self.sd, dtype=torch.float32))
        prob = torch.sigmoid(logit).numpy()
        return dict(comp=100 * comp.numpy(), score=logit.numpy(), prob=prob, decide=(prob > 0.5).astype(int))


# ------------------------------------------------------------------------------------- metrics
def regression_threshold(comp_train_pred, tag_train):
    """Decision from regression: mean + 3 SD of predicted adulterant fraction on training authentic scans."""
    a = 100 - comp_train_pred[tag_train == 0, 0]
    return a.mean() + 3 * a.std(ddof=1)


def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def scores(y, tag, groups, comp, decide, score):
    """Scan-level metrics dict."""
    out = {}
    tp = int(((decide == 1) & (tag == 1)).sum()); tn = int(((decide == 0) & (tag == 0)).sum())
    fp = int(((decide == 1) & (tag == 0)).sum()); fn = int(((decide == 0) & (tag == 1)).sum())
    out.update(tp=tp, tn=tn, fp=fp, fn=fn)
    out["sensitivity"] = tp / (tp + fn) if tp + fn else np.nan
    out["specificity"] = tn / (tn + fp) if tn + fp else np.nan
    out["balanced_accuracy"] = np.nanmean([out["sensitivity"], out["specificity"]])
    out["auc"] = roc_auc_score(tag, score) if len(set(tag)) == 2 else np.nan
    out["r2_tahini"] = r2(y[:, 0], comp[:, 0])
    out["rmsep_tahini"] = float(np.sqrt(((y[:, 0] - comp[:, 0]) ** 2).mean()))
    out["mae_tahini"] = float(np.abs(y[:, 0] - comp[:, 0]).mean())
    for j, c in enumerate(COMP):
        out[f"rmsep_{c}"] = float(np.sqrt(((y[:, j] - comp[:, j]) ** 2).mean()))
    adult = tag == 1
    true_ad = np.where(y[adult, 1] > 0, 1, 2)
    pred_ad = np.where(comp[adult, 1] >= comp[adult, 2], 1, 2)
    out["identification"] = float((true_ad == pred_ad).mean()) if adult.any() else np.nan
    return out


def sample_level(groups, y, tag, comp, score):
    """Average scans of each physical sample (decision re-made on the averaged score/prob)."""
    df = pd.DataFrame(dict(g=groups, tag=tag, s=score))
    for j, c in enumerate(COMP):
        df["y" + c] = y[:, j]
        df["p" + c] = comp[:, j]
    a = df.groupby("g", sort=False).mean()
    return (a.index.to_numpy(), a[["y" + c for c in COMP]].to_numpy(), a["tag"].round().astype(int).to_numpy(),
            a[["p" + c for c in COMP]].to_numpy(), a["s"].to_numpy())


def cluster_bootstrap(groups, fn, n=1000, seed=0):
    """Resample physical samples with replacement; fn(idx) -> dict of metrics. Returns DataFrame."""
    rng = np.random.RandomState(seed)
    ug = np.unique(groups)
    pos = {u: np.where(groups == u)[0] for u in ug}
    rows = []
    for _ in range(n):
        pick = rng.choice(ug, len(ug), replace=True)
        idx = np.concatenate([pos[u] for u in pick])
        try:
            rows.append(fn(idx))
        except ValueError:
            continue
    return pd.DataFrame(rows)


def lod(pred_adult, nominal_adult, tag):
    """LOD = 3.3 sigma / S (Foods convention)."""
    sigma = np.std(pred_adult[tag == 0], ddof=1)
    S = np.polyfit(nominal_adult, pred_adult, 1)[0]
    return 3.3 * sigma / S, sigma, S


def dump(obj, name):
    p = RESULTS / name
    p.write_text(json.dumps(obj, indent=2, default=float))
    return p
