### Declaration
#### Zero-dimensional types (Points 点)

Only contain a value.

| 漢字ット (KanJIT) | Pseudo-code |
|:---------------- |:------------|
| **Boolean**<br>`イ真偽也。` | <br/>`bool i;` |
| **Character**<br/>`イ字也。` | <br/>`char i;` |
| **Integer**<br/>`イ数也。` | <br/>`int i;` |
| **Floating-point number**<br/>`イ分数也。` | <br/>`float i;` |

#### One-dimensional types (Lines 線分)

Contain a value and a horizontal offset.

| 漢字ット (KanJIT) | Pseudo-code |
|:-----------------|:------------|
| **Bitarray**<br/>`イ有無也。` (mutable) | <br/>`bool[];` |
| **String**<br/>`イ言也。` (immutable)<br/>`ロ字々也。` (mutable)<br/>`ハ三字也。` (immutable) | <br/>`str i;`<br/>`char[] ro;`<br/>`char[3] ha;` |
| **Sequence**<br/>`イ番号也。` (mutable)<br/>`ロ集合也。` (immutable)<br/>`ハ数々也。` (mutable)<br/>`ニ分数々也。` (mutable)<br/>`ホ三数也。` or `ホ三列也。` (immutable)<br/>`ヘ三分数也。` (immutable) | <br/>`list<int, float> i;`<br/>`tuple<int, float> ro;`<br/>`int[] ha;`<br/>`float[] ni;`<br/>`int[3] ho;`<br/>`float[3] he;` |
| **Array** <br/>`イ列挙也。` (mutable)<br/>`イ列記也。` (immutable) | <br/>`list<Any> i;`<br/>`tuple<Any> ro;` |

#### Two-dimensional types (Planes 平面)

Contain a value and vertical and horizontal offsets.

| 漢字ット (KanJIT) | Pseudo-code |
|:-----------------|:------------|
| **Bitmap**<br/>`イ経緯也。` (mutable)<br/>`ロ三緯四経也。` (immutable) | <br/>`bool[][];`<br/>`bool[3][4];` |
| **Matrix**<br/>`イ行列也。` (mutable)<br/>`ロ三行四列也。` (immutable) | <br/>`int[][] i;` or `float[][] i;`<br/>`int[3][4] ro;` or `float[3][4] ro;` |
| **Dictionary**<br/>`イ辞書也。` (mutable)<br/>`ロ三辞書也。` (immutable) | <br/>`str[] i;`<br/>`str[3] ro;` |
| **Catalog**<br/>`イ型録也。` (mutable)<br/>`ロ三型四録也。` (immutable) | <br/>`char[][] i;`<br/>`char[3][4] ro;` |

#### Records / Structs / Hashmaps / Others

### Assignment

#### Backassignment
