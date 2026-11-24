# THE WORLD TODAY: 24 November 2026
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/khaliefk/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/khaliefk/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

See the bounty page at https://make.fun/bounty/news-image-20261124.


Entry for the make.fun competition `news-image-20261124`: sum up 24
November 2026's world news in one image.

## What it is

A 1024x1024 JPEG newspaper front page, titled THE WORLD TODAY, drawn with
PIL by `build_image.py`. The lead story is the Russian drone that crossed
into Polish airspace overnight near Dorohusk, with Warsaw scrambling jets.
Four more stories fill the page: Jensen Huang returning to Nvidia as chief
with shares jumping about a third, the EU proposing its 22nd sanctions
package on Russia, an Israeli strike killing a UN aid worker in Gaza, and
ousted Bangladeshi PM Sheikh Hasina planning to fly home on 16 December.
A short "Also today" strip covers Australia's planned tech fines, the CAS
ruling due on Senegal's Africa Cup title appeal, and the Himalayan flood in
India. Every story was reported on 24 November 2026, checked against Reuters
and other wires that morning.

## How it runs

`main.py` is standard library only. It copies the shipped `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR` when set) and checks the file
against the gate: at most 1 MiB, at most 1024x1024 pixels. The copy is byte
for byte, so two runs write identical output.

Rebuild the image any time with:

```
python3 build_image.py
```

Then run the entry with:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py`: the entrypoint, copies `entry.png` to the output directory.
- `entry.png`: the front page image (JPEG bytes, 1024x1024).
- `build_image.py`: the PIL script that drew the front page.
- `LICENSE`: MIT.
