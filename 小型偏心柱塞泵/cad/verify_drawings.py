"""交付物回归校验 — 对 cad/ 下已交付的 DXF/DWG/PDF 逐项断言。

用法： python verify_drawings.py
退出码：0 全部通过；1 有失败项。

校验逻辑：尺寸读数一律取 DXF 中 DIMENSION 实体的 group 42
（线性=长度，角度=弧度），这是唯一可靠的读数途径 —— entity_get 不返回尺寸值。
"""
import os
import sys

CAD = os.path.dirname(os.path.abspath(__file__))
TOL_LIN = 0.02      # mm
TOL_ANG = 0.002     # rad

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("  | " + detail) if detail else ""))


def parse_dxf(path):
    txt = open(path, "rb").read().decode("utf-8", errors="replace")
    lines = txt.splitlines()
    pairs = []
    i = 0
    while i < len(lines) - 1:
        pairs.append((lines[i].strip(), lines[i + 1]))
        i += 2
    ents, cur = [], None
    for code, val in pairs:
        if code == "0":
            if cur:
                ents.append(cur)
            cur = [(code, val)]
        elif cur is not None:
            cur.append((code, val))
    if cur:
        ents.append(cur)
    return ents


def get(e, c):
    return [v for cc, v in e if cc == c]


def audit(tag, fname, expect_lin, expect_ang, expect_hatch, expect_dims):
    print("\n=== %s  (%s) ===" % (tag, fname))
    path = os.path.join(CAD, fname)
    if not os.path.exists(path):
        check(tag + " 文件存在", False, "缺 " + fname)
        return
    check(tag + " 文件存在且非空", os.path.getsize(path) > 10000,
          "%d B" % os.path.getsize(path))

    ents = parse_dxf(path)
    dims = [e for e in ents if "DIMENSION" in e[0][1]]
    lin, ang = [], []
    for e in dims:
        t70 = get(e, "70")
        t70 = int(t70[0]) if t70 else 0
        m = get(e, "42")
        if not m:
            continue
        v = float(m[0])
        # DXF group 70 里带标志位：低 4 位才是尺寸类型
        # 0=linear 1=aligned 2=angular 3=diameter 4=radius；高位是 0x20/0x80 等标志
        dtype = t70 & 0x0F
        if dtype == 2:
            ang.append(v)
        else:
            lin.append(v)

    check(tag + " 尺寸实体数量", len(dims) == expect_dims,
          "实测 %d / 期望 %d" % (len(dims), expect_dims))

    # 线性尺寸：逐个期望值必须在实测集合中命中（双射，防重复/防漏）
    pool = list(lin)
    missing = []
    for want in expect_lin:
        hit = next((v for v in pool if abs(v - want) <= TOL_LIN), None)
        if hit is None:
            missing.append(want)
        else:
            pool.remove(hit)
    check(tag + " 线性尺寸逐项命中", not missing,
          "缺失 " + str(missing) if missing else "全部命中")
    check(tag + " 无多余线性尺寸", not pool,
          "多余 " + str([round(v, 3) for v in pool]) if pool else "无")

    pool = list(ang)
    missing = []
    for want in expect_ang:
        hit = next((v for v in pool if abs(v - want) <= TOL_ANG), None)
        if hit is None:
            missing.append(round(want, 4))
        else:
            pool.remove(hit)
    check(tag + " 角度尺寸逐项命中", not missing,
          "缺失 " + str(missing) if missing else "全部命中")
    check(tag + " 无多余角度尺寸", not pool,
          "多余 " + str([round(v, 4) for v in pool]) if pool else "无")

    hatches = [e for e in ents if e[0][1] == "HATCH"]
    check(tag + " 真实 HATCH 剖面线", len(hatches) >= expect_hatch,
          "实测 %d / 至少 %d" % (len(hatches), expect_hatch))

    # 中文不出现 ?????? （字体样式没配对时的症状）
    texts = []
    for e in ents:
        if e[0][1] in ("TEXT", "MTEXT"):
            s = "".join(get(e, "1"))
            if s:
                texts.append(s)
    bad = [t for t in texts if "?" in t]
    check(tag + " 中文渲染正常（无乱码）", not bad,
          "乱码 " + str(bad[:3]) if bad else "无乱码")

    # spec §9 的 8 个图层必须存在
    want_layers = ["01-轮廓粗实线", "02-轮廓细实线", "03-中心线", "04-虚线",
                   "05-标注", "06-文字", "07-剖面线", "08-图框标题栏"]
    lay_ents = [e for e in ents if e[0][1] == "LAYER"]
    have = set()
    for e in lay_ents:
        n = get(e, "2")
        if n:
            have.add(n[0])
    miss = [n for n in want_layers if n not in have]
    check(tag + " 8 个规范图层齐备", not miss,
          "缺 " + str(miss) if miss else "齐备")


print("交付物回归校验 — cad/")
print("=" * 60)

# BP-05 配流盘：Ø64 / R22.5 / R29.5 / Ø16.5 / 厚10 / 键槽宽4 / 键槽深2.5
audit("BP-05 配流盘", "BP05_配流盘.dxf",
      expect_lin=[64.0, 22.5, 29.5, 16.5, 10.0, 4.0, 2.5],
      expect_ang=[2.7925268, 0.3490659],   # 160°, 20°
      expect_hatch=4, expect_dims=9)

# BP-01 泵体：Ø104 / Ø44 / 56 / Ø20H7 / 12.5 / Ø5 / R26 / Ø92 / 腔深10
audit("BP-01 泵体", "BP01_泵体.dxf",
      expect_lin=[104.0, 44.0, 56.0, 20.0, 12.5, 5.0, 26.0, 92.0, 10.0],
      expect_ang=[2.0943951],              # 120°
      expect_hatch=7, expect_dims=10)

# BP-02 偏心轴：5 个直径 + 8 段长度 + 总长 93 + 键槽宽4/深2.5 + e=2.5 + R12
# 注意 4 出现 2 次（4mm 段 + 键槽宽）、12 出现 4 次（3 个 12mm 段 + R12）、2.5 出现 2 次
audit("BP-02 偏心轴", "BP02_偏心轴.dxf",
      expect_lin=[16.0, 13.0, 20.0, 24.0, 16.0,
                  10.0, 2.0, 17.0, 12.0, 12.0, 12.0, 4.0, 24.0, 93.0,
                  4.0, 2.5, 2.5, 12.0],
      expect_ang=[],
      expect_hatch=0, expect_dims=18)

# BP-00 装配图：外形 Ø104 / 总高 74 / 轴伸 6 / 中心腔 Ø44 / 偏心距 e=2.5
audit("BP-00 装配图", "BP00_装配图.dxf",
      expect_lin=[104.0, 74.0, 6.0, 44.0, 2.5],
      expect_ang=[],
      expect_hatch=20, expect_dims=5)

# 三件套齐全性
print("\n=== 交付三件套 ===")
for stem in ["BP05_配流盘", "BP01_泵体", "BP02_偏心轴", "BP00_装配图"]:
    for ext in [".dwg", ".dxf", ".pdf"]:
        p = os.path.join(CAD, stem + ext)
        ok = os.path.exists(p) and os.path.getsize(p) > 1000
        check(stem + ext, ok,
              ("%d B" % os.path.getsize(p)) if os.path.exists(p) else "缺失")

failed = [r for r in RESULTS if not r[1]]
print("\n" + "=" * 60)
print("结果：%d 项通过 / %d 项失败" % (len(RESULTS) - len(failed), len(failed)))
if failed:
    for n, _, d in failed:
        print("  FAILED:", n, d)
    sys.exit(1)
print("全部通过 (ALL GREEN)")
