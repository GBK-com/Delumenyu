# AutoCAD 全套工程图 — 交付现状（2026-11-02 12:30 全部完成）

负责人：sub-cad　｜　任务板：task-4
依据：`spec/DESIGN_SPEC.md` **v1.1 + Lead 更正 #1/#2 + v1.3**（见文末"取值口径"）

**总览：4 张图全部完成并交付。四张均通过 `drawing_finalize`（0 error），各 **92/100，等级 B**。**
回归校验 `py -3 verify_drawings.py` → **48 项通过 / 0 项失败（ALL GREEN）**。

---

## 1. 逐图状态

| 图号 | 图名 | 状态 | 图幅/比例 | 实体/尺寸数 | 文件 |
|---|---|---|---|---|---|
| BP-05 | 配流盘 | **完成** | A3 / 2:1 | 228 / 9 | `cad/BP05_配流盘.dwg` `.dxf` `.pdf` |
| BP-01 | 泵体 | **完成** | A3 / **1:1**（见 §7） | 248 / 10 | `cad/BP01_泵体.dwg` `.dxf` `.pdf` |
| BP-02 | 偏心轴 | **完成** | A3 / 1:1 | — / 18 | `cad/BP02_偏心轴.dwg` `.dxf` `.pdf` |
| BP-00 | 装配图 | **完成** | **A1** / 1:1 | 24 HATCH / 5 | `cad/BP00_装配图.dwg` `.dxf` `.pdf` |

文件绝对路径与大小：
```
C:\Users\谷博康\Desktop\sw\cad\BP05_配流盘.dwg   32,879 B
C:\Users\谷博康\Desktop\sw\cad\BP05_配流盘.dxf  157,348 B
C:\Users\谷博康\Desktop\sw\cad\BP05_配流盘.pdf   63,654 B
C:\Users\谷博康\Desktop\sw\cad\BP01_泵体.dwg     30,721 B
C:\Users\谷博康\Desktop\sw\cad\BP01_泵体.dxf    159,300 B
C:\Users\谷博康\Desktop\sw\cad\BP01_泵体.pdf    125,662 B
C:\Users\谷博康\Desktop\sw\cad\BP02_偏心轴.dwg   29,157 B
C:\Users\谷博康\Desktop\sw\cad\BP02_偏心轴.dxf  156,902 B
C:\Users\谷博康\Desktop\sw\cad\BP02_偏心轴.pdf  123,082 B
C:\Users\谷博康\Desktop\sw\cad\BP00_装配图.dwg   48,688 B
C:\Users\谷博康\Desktop\sw\cad\BP00_装配图.dxf  349,764 B
C:\Users\谷博康\Desktop\sw\cad\BP00_装配图.pdf  160,244 B
```

---

## 2. BP-05 配流盘（完成）

- 图幅 A3 / 比例 2:1（几何 ×2，DIMLFAC=0.5，DIMSCALE=2，**已实测校验：Ø128 几何显示 Ø64**）
- 视图：主视图（Ø64 外形 + 2 个**真实 ARC 腰型窗** + 中心孔 Ø16.5 + 键槽 4×2.5）、A-A 剖视（沿 Y 轴剖，4 条材料带 + 4 处真实 HATCH）
- 腰型窗几何：内 R22.5 / 外 R29.5，包角 **160°**，岛 **20°**，岛跨 ±X 轴；窗 A 压油 α∈[10°,170°]，窗 B 吸油 α∈[190°,350°]（按 `data/portplate_geometry.md`）
- 实体统计（DXF 解析）：LINE 89 / ARC 8 / LWPOLYLINE 19 / CIRCLE 3 / HATCH 5 / DIMENSION 9 / TEXT+MTEXT 65 / TABLE 9
- **真实尺寸标注 9 个**，DXF group-42 逐条校验全部正确：
  Ø64 = 64.0 ｜R22.5 = 22.4995 ｜R29.5 = 29.5000 ｜160° = 2.79274 rad ｜20° = 0.34886 rad ｜Ø16.5 = 16.5 ｜厚 10 = 10.0 ｜键槽宽 4 = 4.0 ｜键槽深 2.5 = 2.5
- 形位公差（原生 `gd_frame`）：平行度 0.005 A、平面度 0.005、垂直度 Ø0.01 A、位置度 Ø0.05 B、对称度 0.02 B ＋ 基准 A/B（`datum_feature`）
- 表面粗糙度（原生 `surface_texture`，ISO 21920-1）：Ra0.4 ×2（两配流面）、Ra1.6（Ø16.5 孔）
- 技术要求 5 条（全中文）＋ 窗A/窗B 标注
- `drawing_critique`：空（无告警）｜`validation_check`：11 条 **info**（空图层）｜`drawing_finalize`：**92 分 / B**，0 error，1 warning
  - 唯一 warning = `fake_dimension_text`，命中 3 个 TEXT（`Ø0.01`、`Ø0.05` 两个**形位公差直径带前缀**、`4. 未注倒角 C0.5；未注圆角 R0.8；` 这条技术要求）。**属启发式误判**：真实尺寸全部是 DIMENSION 实体，这 3 个是标注文字/公差带前缀，非假标注。

---

## 3. BP-01 泵体（完成）

- 图幅 A3。
- 视图：主视图（外形 + 内部虚线）、俯视图（Ø104 / Ø44 腔 / Ø64 配流面 / Ø92 螺栓圈 / 3 柱塞孔 / 3 配流孔 / 2 油口）、**B-B 全剖**（7 处真实 HATCH）
- 实体统计（DXF 解析）：LINE 95 / ARC 3 / LWPOLYLINE 24 / CIRCLE 15 / HATCH 7 / DIMENSION 10 / TEXT+MTEXT 66 / TABLE 9
- **真实尺寸标注 10 个**，DXF 逐条校验：
  Ø104 = 104.0 ｜Ø44 = 44.0 ｜高 56 = 56.0 ｜Ø20H7 = 20.0（带 H7 公差代号）｜3×Ø12.5 孔宽 = 12.5 ｜Ø5 = 5.0 ｜R26 = 26.0 ｜Ø92 = 92.0 ｜腔深 10 = 10.0 ｜120° = 2.09439 rad
- 形位公差（原生 `gd_frame`）：圆柱度 0.006、圆柱度 0.008、垂直度 Ø0.01 A、平面度 0.008、位置度 Ø0.02 A B、圆度 0.03 ＋ 基准 A/B
- 粗糙度：Ra0.8 ×2（配流面 / 柱塞孔）、Ra3.2（Ø104）
- 技术要求 5 条（全中文）；3 处引线文字（3×Ø12.5 120°均布 / 6-M5 深12 均布 / 2-M14×1.5 吸压油口）
- `drawing_critique`：空｜`validation_check`：仅 info｜`drawing_finalize`：**92 分 / B**，0 error，1 warning（同上 `fake_dimension_text`，6 个 TEXT 命中，性质相同）

---

## 4. BP-02 / BP-00 制作要点（2026-11-02 已完成，供复核）

### BP-02 偏心轴（A3 / 1:1，92 分 / B，18 个真实尺寸）
- 主视图：9 段阶梯闭合轮廓 + 两处键槽（z −12→−4、z 70→78，均居于 +X 母线，键槽底 R5.5）+ 退刀槽 Ø13×2
- 键槽断面图：Ø16 圆弧断开 + 键槽矩形（4 宽 × 2.5 深）
- 偏心轮端视图：R12 偏心圆（中心偏移 2.5）+ Ø20 轴颈虚线 + **e=2.5±0.02 用真实公差样式**（`dimstyle_create` 覆盖 `DIMTOL=1, DIMTP=DIMTM=0.02` 做成 ISO-TOL，再切回 ISO-1X）——不是文字假标注
- 形位公差：圆柱度 0.005、同轴度 Ø0.01 A-B、圆跳动 0.02 A-B、键槽对称度 0.02 A-B；Ra0.4 / Ra0.8
- 18 个尺寸全部 DXF 逐项校验通过

### BP-00 装配图（A1 / 1:1，92 分 / B，5 个关键尺寸）
- **主视图**（外形 Ø104×74、轴伸 6、油口 Ø14 于 z=40、6 颗 M5 头投影 4 处）
- **A-A 全剖**（过轴线竖直全剖，35 个轮廓实体 + 24 处真实 HATCH，四种 pattern 区分零件：泵体 ANSI31 / 配流盘 ANSI33 / 回程盘 ANSI32 / 端盖 ANSI37）
- **配流原理图**（右上角，Ø64 盘 + 2 个 160° 腰窗 + 20° 岛 + 0/120/240 柱塞射线 + 相位表 + 说明）
- 序号引线 11 项（圆 + 数字 + 引线，全部手拼实体，`mleader` 工具是坏的）
- 明细栏 12 行 6 列（`entity_create_table` 原生 TABLE 实体），按 v1.3 值：M5×30×3 / M5×20×3 / O 型圈 67×3×2 / 弹簧 自由长17、总圈8/有效6
- 技术要求：客户原文 5 条一字不改 + 追加 2 条 + **弹簧未绘出声明**（按要求如实标注，明细栏仍列 ×3）
- **未做**：柱塞方位剖视图（Lead 允许砍）、6 颗 M5 的逐颗剖面区分（剖切面只过 0° 一颗）


### BP-02 偏心轴（A3 / 1:1，最简单，建议先做）
- 主视图：9 段阶梯轮廓，总长 93；Ø16/Ø13（退刀槽）/Ø20/Ø24（偏心轮 e₁=2.5，z16–28）/Ø20/Ø20（平衡偏心 e₂=1.2，z40–52）/Ø20/Ø16；两处键槽 4×2.5（z −12→−4、z 70→78）
- 键槽断面图（4×2.5）；偏心轮端视图（标 R12 与偏心距 2.5±0.02）
- 形位公差（§6）：Ø20h6 圆柱度 0.005、同轴度 Ø0.01（基准 A-B）、Ra0.4、偏心轮圆跳动 0.02、键槽对称度 0.02
- 技术要求：材料 45，调质 HB220~250；未注倒角 C1；未注圆角 R0.8（轴肩 R1）

### BP-00 装配图（A1 / 1:1，最重要）
- 主视图（外形 Ø104×68，轴伸 Ø16 长 12 露出端盖）
- **A-A 全剖**（过轴线竖直全剖）：需剖到 泵体/偏心轴/柱塞/回程盘/配流盘/端盖/螺钉/O 型圈；剖面线相邻零件方向相反
- 柱塞方位剖视图（过 0° 柱塞轴线的水平剖）
- 序号引线 **11 项**（对应明细栏 §4）
- 明细栏（序号/代号/名称/数量/材料/备注）＋ 标题栏「小型偏心柱塞泵（装配图）」1:1 图号 BP-00
- 技术要求：spec §5 **原文一字不改** 5 条 ＋ 追加 2 条
- 关键尺寸：Ø104、总高 68、Ø92/6-M5、偏心距 2.5、柱塞行程 5
- 另需「配流原理图」小块（Lead 更正 #2 要求，装配图右上角）：窗A/窗B/两个 20° 岛 + 柱塞 0/120/240 射线 + 相位表 + 说明文字

---

## 5. 取值口径（明日务必沿用，勿再用旧值）

| 项 | **现行值** | 作废值 |
|---|---|---|
| 泵体中心腔 | **Ø44**（z 10→56） | Ø30 |
| 泵体柱塞孔 | **R22 → R48** | R15 |
| 泵体配流孔 | **Ø5 @R26**（z 0→22） | R19 |
| 泵体下端配流面 | **Ø64** | Ø56 |
| 泵体 2×油口 | **M14×1.5，方位 90°/270°，轴线 z=40** | 60°/300° |
| 泵体体积 | **376,159.16 mm³** | 376,298.31 |
| 配流盘 | **Ø64×10**，腰型窗 内R22.5/外R29.5，**包角160°/岛20°** | Ø56，110°/70° |
| 端盖密封槽 | **Ø70 中径**，宽 3.8，深 2.4 | Ø88 / Ø78 |
| 回程盘密封槽 | **Ø70 中径** | Ø88 / Ø78 |
| O 型圈（端盖+回程盘） | **67×3，数量 2**（明细栏序号 10） | 88×3 / 75×3 |
| 回程盘备注 | **「上端封压盘，球面自定心」** | 「球面自定心」 |
| 弹簧 | 线径 Ø1.6，中径 Ø10，**自由长 17，有效圈 8**，安装长 10.5~15.5 | 自由长 21、7 圈 |
| 偏心轴 | 不变（总长 93，26,474.29 mm³） | — |
| 装配总高 | **74**（不含轴伸），外径 Ø104 | 68 |

---

## 6. 工具经验（明日直接用，省大量试错时间）

### 6.1 必须知道的流程约束
1. **AutoCAD MCP 只能写 `D:\AutoCad`**（`ALLOWED_PATHS`）。`drawing_save` / `drawing_export_*` 传工作区路径会被拒。做法：先存 `D:\AutoCad\<ascii名>.dwg`，再用 `ops_bash` `cp` 到 `cad/`（中文文件名在 cp 目标端给）。
2. **同名覆盖保存会报 COM 错**（`0x7ffdfff7 发生意外`）。**每次保存换一个新文件名**（如 `BP05_portplate.dwg` → `_v2`），再 cp 成中文名。
3. **中文必须先建字体样式再画字**：`textstyle_create{name:"HZ", font:"simsun.ttc"}` → `textstyle_set_current{name:"HZ"}`，**然后**才 `titleblock_apply` 和写 TEXT。否则 ISOCP 无中文字形，全部渲染成 `??????`（本次踩过，已修）。
4. `drawing_finalize` 前必须已 `drawing_save`，否则报 `not_saved`。

### 6.2 好用的工具（放心用）
- `entity_batch_create`：一次画几十个实体，`type` 支持 **line / circle / arc / polyline / text**，每个实体可带 `layer`。
- `entity_batch_modify`：`operations:[{action:"delete"|"move", handle, dx, dy}]`，批量删/移。
- `entity_set_properties{handle, layer}`：改单个实体图层（batch_modify **没有**改图层 action，`restyle`/`set_layer` 都不认）。
- `gd_frame{symbol, tolerance, x, y, datums[], layer}`：真 ISO 1101 框格。**symbol 合法值**：angularity / circular_runout / circularity / concentricity / cylindricity / flatness / parallelism / perpendicularity / position / profile_line / profile_surface / straightness / symmetry / total_runout（**圆度是 `circularity`，不是 roundness**）。
- `datum_feature{letter, x, y, layer}`、`surface_texture{x, y, ra}`（ISO 21920-1）、`entity_create_hatch{pattern, boundary_points, layer}`、`titleblock_apply{title, drawing_no, size:"A1"/"A3", scale, material, part_no}`、`dimension_linear/aligned/diameter/radius/angular`、`view_zoom_window` + `view_screenshot`（校准坐标用）。

### 6.3 坑（务必避开）
1. **`dimension_linear` 对竖直尺寸（x1==x2）会测成 0** → 竖直尺寸一律用 `dimension_aligned`。本次已踩，BP-05 的厚度 10、键槽宽 4 都是这么救回来的。
2. **`dimension_radius` 的 chord 点必须精确落在圆弧上**，否则出现 `22.51` 这类四舍五入垃圾（要用 `R·cosθ, R·sinθ` 算到小数点后 4 位）。
3. **`dimension_angular` 会量成补角**：1° 拔模角量出来是 179°，换 text 位置也没救。**小角度不要用角度标注**，改用引线 + 文字（BP-01 的 1° 拔模就是这么处理的）。
4. **`gd_frame` 的 tolerance 只收数字**，不能写 `"Ø0.01"`。要 Ø 前缀：拿到返回 handles 里第 5 个（`[polyline, div, div, symbol, tolerance, datum]`）删掉，再 `entity_create_text` 写 `"Ø0.01"`（高度 2.4 刚好塞进 7.17 宽的格）。
5. **`leader_create_mleader` 是坏的**：COM 报 `'tuple' object has no attribute 'TextString'`。引线一律用 `entity_create_line` + `entity_create_text` 拼（序号引线、粗糙度引出都一样）。
6. **`entity_create_hatch` 不接受 `scale`/`pattern_scale`**（COM 错），剖面线间距不可调；**也没法设角度**，所以"相邻零件剖面线方向相反"这条**做不到**——只能用不同 pattern（ANSI31/ANSI32/ANSI33）在视觉上区分零件，需在交付说明里如实写。
7. **`entity_create_polyline` 不接受 `bulges`** → 真圆弧必须用独立 `ARC` 实体（腰型窗就是这么画的）。
8. **一次批量写很多中文 TEXT 会撞 `RPC_E_CALL_REJECTED`**（被呼叫方拒绝接收呼叫）→ 拆成单条重发即可，重发能成功。
9. **`entity_get` 不返回尺寸数值**。**唯一可靠的读数办法：导出 DXF，解析 DIMENSION 的 group 42**（角度存弧度）。每次 finalize 前都该跑一遍。
10. `drawing_understand` 能读全图实体/图层/文字标签，做体检很好用；`analysis_find_in_region` 会报 COM 错，别用。

### 6.4 已验证的比例方案（照抄即可）
- **2:1 图**：几何坐标 ×2 绘制，`dimstyle_create` 覆盖 `DIMLFAC=0.5, DIMSCALE=2, DIMTXT=3.5` → 显示值正确（实测 Ø128 显示 Ø64）。
- **1:1 图**：`DIMLFAC=1, DIMSCALE=1`。
- **泵体无法用 2:1**：Ø104 件两个视图在 A3 上需 416mm＞可用 400mm，故用 **1:1**（spec §9 允许"2:1 或 1:1，按图幅适配"）。此 Deviation 需写入交付说明。

---

## 7. 已知缺陷/Deviation 清单（交付说明要如实写）

1. **图框/标题栏图层**：`titleblock_apply` 把图框与标题栏画在它自带的 `TITLEBLOCK` / `TEXT` 图层，**不接受指定图层**；`08-图框标题栏` 图层已按 spec 建好但为空置。属工具能力限制。
2. **装配图剖面线方向**：见 §6.3-6，无法让相邻零件剖面线反向。
3. **形位公差 Ø 前缀**：用 TEXT 补写（非框格原生），见 §6.3-4。
4. **泵体 1° 拔模**：用引线文字「1° 拔模（沿 +Z 出模）」而非角度尺寸，见 §6.3-3。
5. **`fake_dimension_text` warning**：两张图各 1 条，为启发式误判（详见 §2 末）。
6. **BP-02 / BP-00 未出图**。

---

## 8. 交付物回归校验（可重复运行，只读文件，不碰 AutoCAD）

```bash
cd cad && py -3 verify_drawings.py      # 退出码 0 = 全绿
```

最近一次运行：**24 项通过 / 0 项失败（ALL GREEN）**

覆盖内容：
- 两张图 DIMENSION 实体数量（BP05=9、BP01=10）与**逐项数值命中**（按 group 42 读数，线性容差 0.02mm、角度容差 0.002rad）
- **无多余/重复尺寸**（这条曾抓出 BP05 重复的 R22.5）
- 真实 HATCH 数量（BP05≥4、BP01≥7）
- 中文无 `??????` 乱码（字体样式配错时的症状）
- spec §9 八个图层齐备
- DWG/DXF/PDF 三件套存在且非空

> ⚠️ 写新图时请把它读作"回归基线"：出完新图后把该图的期望尺寸列表加进脚本，
> 跑一遍再交付。**不要只靠肉眼看 PDF** —— 本次三次真实缺陷（竖直尺寸测成 0、
> R29.5 被误删成重复 R22.5、补角量出 179°）全是脚本读数抓出来的。

> 脚本自身的坑（已修）：DXF `DIMENSION` 的 group 70 带标志位，
> **低 4 位才是尺寸类型**（0=linear 1=aligned 2=angular 3=diameter 4=radius），
> 直接跟 2 比较会把角度误判成线性（34 & 0x0F == 2）。

---

## 9. 明日第一步建议


1. 先做 **BP-02 偏心轴**（1 张 A3、1:1、约 40 个实体，最快出成果）。
2. 再做 **BP-00 装配图**（A1）：先把 A-A 全剖的零件轮廓按 §5 取值画出来 → 7~10 处 hatch → 11 个序号（line+circle+text 手拼）→ `entity_create_table` 出明细栏 → 技术要求原文 → 最后补柱塞方位剖视与配流原理图。
3. 每张出完立刻 `drawing_save`（新文件名）→ 导 DXF → **解析 group 42 校验尺寸** → `drawing_finalize` → 导 PDF → cp 到 `cad/`。

---

## 10. 2026-11-02 新增经验（在做 BP-02 / BP-00 时踩到）

**新增的坑：**
1. **批量实体上限约 8~10 个**：一次发 29 个实体时 20 个被 `RPC_E_CALL_REJECTED` 拒掉（且**前一个还报了 `AddLine.ObjectName` 但实际创建成功**，导致我以为没建、重发后产生**重复线**）→ 结论：**批量 ≤8 个**；报错后**先查再重发**，不要盲目重发。
2. `drawing_finalize` 的 `duplicate_entities` 检查能抓出这类重复实体（本次抓到 2B3/2B6 重复线，删掉后 84→92 分）。**这是第二道防线，别只信自己的记忆。**
3. `dimension_*` **没有 `tolerance` 参数**（传 `"±0.02"` 直接 schema 报错）。要真公差：`dimstyle_create` 覆盖 `DIMTOL=1, DIMTP=0.02, DIMTM=0.02` 建专用样式 → `dimstyle_set_current` → 画该尺寸 → 切回原样式。**这是唯一的"真公差"路子，比文字补 ±0.02 干净。**
4. `drawing_new` 偶尔报 `Add.Name`（AutoCAD 刚启动/有模态）→ **直接重试一次**即可成功。
5. `drawing_apply_standard` 也可能被拒（`could not read INSUNITS`）→ 重试；它失败时**字体样式没被重置**，所以 `textstyle_set_current HZ` 仍要放在它之后。
6. AutoCAD 窗口最小化时 `view_screenshot` / `view_zoom_and_screenshot` 会返回 159×27 的空白图 → **不是图纸坏了**，别据此判断；以 PDF + DXF 解析为准。

**新增可用能力：**
7. `entity_create_hatch` 支持 **ANSI31 / ANSI32 / ANSI33 / ANSI37**——相邻零件用不同 pattern 可视觉区分（虽仍无法设角度，"方向相反"这条做不到）。
8. `dimension_diameter` 传**上下两个对称点**（如 (95,208)-(95,192)）即可在轴类侧视图上生成**轴向直径标注**（Ø16），不必依赖圆实体。
9. `titleblock_apply{size:"A1"}` 正常出 841×594 图框；标题栏仍固定落在 `TITLEBLOCK`/`TEXT` 图层（`08-图框标题栏` 空置，属工具限制，已在 §7 记录）。
10. `entity_create_table{rows:[表头,...]}` 出原生 TABLE；12 行 6 列约 120×84 mm，从 (x,y) 向下生长，注意别压标题栏。

**一处必须记住的几何校核（本次自己抓出的错）：**
装配图 A-A 剖里，偏心轮画成 +2.5 偏心 ⇒ 对应 **θ=0**，此时柱塞必须在 **ρ=19.5**（球心），球头最内点 14.5 恰与偏心轮包络相切。**我一开始按 ρ=17（中位）画，球头插进偏心轮 2.5mm——是自己画出的干涉**，发现后整体右移 2.5 修正。
⇒ 规律：**画剖视前先确认"这个视角对应哪个 θ"，再算 ρᵢ = 17 + 2.5·cos(θ−φᵢ)**，否则必出假干涉。

