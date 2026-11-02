# REF: Tanraak + Black-rat TF Knowledge Pack
**For:** Jack → female Anubis (bipedal) ComfyUI gens  
**Date:** 2026-11-02 Asia/Hong_Kong  
**Sources (Felix machine):**
1. `C:\Icloud\iCloudDrive\文稿\Logs\Patcher Logs\Uplay\Uplay\Collect\Tanraak` — **39** jpg
2. `...\Collect\Black-rat` — **1103** files (1051 jpg/png/jpeg usable; 52 bmp skipped; ~55 originals >20MB skipped at staging)

**Staging:** `Downloads\_grok_tf_refs\tanraak|blackrat|blackrat_sheets` → box `/workspace/tf_refs/`  
**Jack clothes lock (project):** purple short-sleeve tee + khaki shorts + sneakers; **no gold jewelry**; end = bipedal female Anubis; 8-frame arc per `tf-sequence-frame-content.md`.  
**Do not upload full image binaries to GitHub** — this md (+ thin README) only.

> **UPDATE (2026-11-02 HKT):** Fel correction — primary need is **character reactions/actions during TF**, not species taxonomy.  
> New focused doc: [`REF_TF_reactions_actions.md`](./REF_TF_reactions_actions.md)  
> Project mirror: `/workspace/tf-deliverables/ref-tf-reactions-actions.md`  
> Covers: face/gaze/hands/posture, clothes-as-action pipeline, species-agnostic mechanics, Jack 8-frame reaction recipe, oversized Black-rat fine-reads. **This file kept** as pack inventory / species notes (extend, do not delete).


---

## 1. Pack overview

| Pack | Count | What it is | Jack usefulness |
|---|---|---|---|
| **Tanraak** | 39 | Four artist mini-series + two Illustrations: bedroom blue-dragon TF; latex wolf TF; cave egg→green dragon "D"; tomb Anubis "J"; gloss Anubis stills | **Highest:** J1–J10 + D clothing-burst mechanics + Illustration endforms. Species mismatch on dragon/latex. |
| **Black-rat** | 1103 | Huge BlackRat / fan-comic dump: canine/werewolf, Sonic-werebeast, feline, dragon, misc. Contact sheets for 17 named series. | **Mechanics library:** seam-burst, digitigrade, muzzle push, muscle hypertrophy, quad drop. Many wrong-species → harvest process tags only. |

### Tanraak inventory (all on box under `/workspace/tf_refs/tanraak/`)
| Series | Files | End species | Sex arc | Clothes in-source |
|---|---|---|---|---|
| `tanraak_1`–`9` | 9 | Blue anthro dragon | male hyper | white tee + jeans → scraps (bedroom) |
| `latexshiftingvixen1`–`4` | 4 | Gloss/latex wolf/herm | male→herm/latex | latex-skin focus |
| `D1`–`D14` | 14 | Green dragon (cave egg trigger) | male muscular → dragon | **purple tee + khaki + red sneakers** (best clothes map) then post-TF sex D13–14 |
| `J1`–`J10` | 10 | Black Anubis/jackal (tomb statue) | male→female Anubis | purple tee + **blue jeans** + red sneakers → shredded; end nude + gold |
| `Illustration.jpg` / `Illustration2.jpg` | 2 | Hyper muscular female black Anubis | female | nude / white+blue scraps; gold jewelry |

### Black-rat staging notes
- Staged under-20MB: **996** files (~1.0 GB) in Downloads `_grok_tf_refs\blackrat`
- Contact sheets (**17**): `sheet_*.jpg` in `blackrat_sheets/` — all copied+vision-read on box
- Oversized skipped (~55): ALM / Muslekitty / Sparecustomes / Zeroora / etc. (rebuild sheets later if needed)

---

## 2. Tanraak beat sheets

### 2.1 `tanraak_1`–`9` — male human → blue dragon (bedroom)
| file | stage | cues | useful tags | IGNORE |
|---|---|---|---|---|
| 1 | pre | lean male, glasses, nude bedroom, discarded jeans/socks | nude human male, glasses, messy room | dragon end; hyper erect focus |
| 2 | early multipanel | claw/scale knuckles, slit pupils budding, horn buds | claw progression, scale spread knuckles | species |
| 3 | mid | blue-grey scales, fin ears, yellow eyes, crouched on chair | mid-TF, discarded clothes pile | dragon ≠ Anubis |
| 4–5 | late | full snout, digitigrade, dorsal ridge, torn jeans remnants | digitigrade feet, clothes burst, rim light | male dragon end |
| 6–7 | macro | hulking fills room, wings, fabric scraps | macro growth, room crush | latex sheen; wings |
| 8–9 | post | full blue dragon pose variants | post-TF power pose | wrong species |

**Map to Jack:** only **clothes-discard / digitigrade / mid-spread pacing**. Not species or latex sheen.

### 2.2 `latexshiftingvixen1`–`4`
Glossy rubber/latex canine/herm TF. High specular black skin, sheath/herm cues.  
**IGNORE entirely for Jack Anubis fur pipeline** except as negative example: `latex, rubber skin, shiny vinyl, herm sheath` → NEG or do-not-copy.

### 2.3 `D1`–`D14` — cave egg → green dragon (best **clothes-damage** ref)
| pages | beat | clothes / body | Jack map |
|---|---|---|---|
| **D1** | setup | blonde+glasses, **purple tee + khaki**, cave; finds glowing scaled egg; reaches | human anchor clothes lock (map khaki→khaki shorts); **Fel rule: do NOT draw statue/egg touch as trigger** — steal wardrobe only |
| **D2–D4** | early–mid | scales on arms/chest; purple tee strains; khaki tears; claws | seam tension → horizontal stress lines before rip |
| **D5** | foot focus | olive scales; **red/white sneakers burst**; white socks shred; khaki shredded to knees; digitigrade talons | **sneaker POP reference** (keep Jack sneakers color/style; claws black not green) |
| **D6–D8** | late / quad | green dragon bulk; khaki as thigh/calf straps; bipedal→all-fours; cave | strap-rags around thick limbs; Jack quad only as brief kneel (frame 7) not feral pages |
| **D9–D12** | dragon completion / power | full green dragon, blonde tuft remains, cream belly | keep "hair remnant" idea for Jack blonde; species ignore |
| **D13–D14** | post-TF sex | green bottom × black/purple latex-shine top dragon; oral→mount | **IGNORE** for Jack TF sequence (wrong cast, latex top, male/male) |

**Prompt tags to harvest:** `purple t-shirt stretching, khaki fabric shredding into straps, red sneakers bursting at toe and sole, white sock shreds, claw punch-through shoe, digitigrade lift heel, muscle bursting seams`

### 2.4 `J1`–`J10` — tomb Anubis TF (**closest species match**)
| file | beat | sex / body | clothes | IGNORE |
|---|---|---|---|---|
| **J1** | trigger | male blonde glasses; statue touch → black gloss claw spreads from hand; fangs | purple tee + **blue jeans** | statue-touch trigger (Fel: no touch); jeans→map to khaki shorts; gloss latex look |
| **J2** | early–mid | dark fur arms; ears migrate; fangs; glowing blue eyes; claws through **red sneakers** | purple tee shredding; sneakers burst | jeans; latex sheen |
| **J3** | mid female lean | black fur arms/neck; glasses fall; tears purple tee open → breasts; thin brown tail from jeans; abs | horizontal purple shreds; jeans thigh tears | jewelry none yet |
| **J4** | genital rewrite | muscular dark canine; knotted phallus → retract → **vulva** through torn crotch | shredded purple + burst jeans crotch | hyena lean if any; keep Anubis |
| **J5** | late female Anubis lean | jet-black short fur, tan muzzle marks, blonde pixie, blue eyes, large breasts, short tail | purple reduced to strip; jeans low/shred; sneakers destroyed | latex oily sheen |
| **J6** | digitigrade / all-fours cue | brown-black fur; full muzzle; paw pads; jeans horizontal calf strips; sneakers sole-split | map jeans strips → khaki strip rags | prolonged quad |
| **J7** | muzzle + gold ear bands | glossy black; gold inner-ear banding; breasts; purple shirt on floor | pants strips | **gold ear bands / jewelry** |
| **J8** | feral lean + collar | all-fours; tan tail; blue fabric ribbons; golden collar + forehead gem forming; neon blue eyes; roar | blue scraps | gold collar/gem; feral |
| **J9** | post power | hyper muscular female black Anubis; gold armbands/collar/forehead; nude flex | none | **all gold jewelry** |
| **J10** | final sheet | latex-black female Anubis; orange eyes variant; gold bands; crouch power pose | none | jewelry; latex; eye-color drift (prefer Jack blue) |

**J→Jack 8-frame mapping (approximate):**
| Jack frame | Borrow from J | Adjust |
|---|---|---|
| 1 human | J1 human panels (wardrobe only) | khaki shorts not jeans; no statue |
| 2 onset | J1 claw-from-contact / fingertip black | no idol; partial hand only |
| 3 early | J2 ears+fangs+tee strain | shorts not jeans |
| 4 rise | J2–J3 shirt shred + breast + tail bud | khaki stress at crotch/hips |
| 5 irreversible | J4 crotch burst + genital rewrite start | **khaki shorts** burst (Fel lock) |
| 6 climax | J4 finish vulva + J5 topless shreds | keep residual purple scraps |
| 7 reshape | J6–J7 muzzle elongate + kneel | brief kneel not feral pages; **strip gold** |
| 8 end | Illustration / J9–10 pose energy | **nude, no jewelry**, bipedal, blue eyes, matte/short fur not latex |

### 2.5 Illustrations
- **Illustration.jpg:** finished hyper-muscular female black Anubis, blue eyes, large breasts, vulva, digitigrade, gold forehead medallion + bicep band, glowing gold ring BG. → **endform body ref**; strip jewelry in prompts.
- **Illustration2.jpg:** same base + **white/blue shredded outfit scraps** (burst-out trope) + gold. → **post-burst residual cloth** ref; still strip gold.

---

## 3. Black-rat series (by contact-sheet / filename patterns)

Visioned via 17 contact sheets. Grouped for Jack relevance.

### 3.A High-value canine / clothing-burst (steal mechanics)
| sheet / pattern | species end | sex | TF lessons for Jack |
|---|---|---|---|
| `sheet_TF_comic_BlackRat` | grey werewolf | male | navy tee vertical shred; digitigrade; moon rim-light; bone CRACK pacing |
| `sheet_rubwulf` | grey/white female wolf | m→f | red shirt chest-burst→breasts; jeans shred; sneakers→digitigrade; gender+muscle parallel |
| `sheet_adoptawuff` | tan/white husky-wolf | female | bite trigger; pink tank/shorts seam shred; slippers pop; bushy tail FLOOMF |
| `sheet_werewolfboy` | feral wolf | male | underwear strain; hand→pad; plantigrade→digitigrade heel-lift; muzzle push anatomy |
| `sheet_AlteredGirl` | muscular anthro canine | fem lean | mirror onset; tank stretch; split paw-pad studies; V-taper back; bushy tail |
| `sheet_alteredmom` | grey muscular canine/hyena | female | button-pop shirt; pec/breast expansion; clawed digitigrade; cramped-in-panel scale |
| `sheet_werefox` | red fox anthro | male | blue shirt shred; black sneakers→dark stockings paws; green slit eyes; white belly pattern |

### 3.B Sonic / game-mascot werebeasts (mechanics only; wrong IP/species)
| sheet | notes |
|---|---|
| `werehog_prime`, `silverhogwolf`, `americanwerehog`, `weretails`, `wolfknux`, `turned_up_to_11`, `sallywolf` | glove/boot/sneaker POP; mega-paw pads; muscle+mane; cargo/vest shred. **Do not copy Sonic IDs, quills, Lombax, chipmunk.** Reuse: seam-burst footwear, pad closeups, roar pose energy. |

### 3.C Wrong-species / specialty (ignore or NEG)
| sheet / patterns | reason |
|---|---|
| `werepanther`, feline sheets | feline muzzle/ears |
| `signs` (red horned beach beast) | dragon/beast + horns |
| Filename clusters: `Trexification_`, `Sorceressdragon_`, `NotFreyaDragonbgs_`, `dragowarfem*`, `weredrago_`, `Deer*`, `KFbunnies_`, `Easterbunny-`, `kittycatburgular_`, `Musletiger_`, `Pokehaus-`, `Barbacorns_` | dragon/dino/deer/bunny/feline/pokemon — process tags only if any |
| `LadiesNight-`, `Beastgurl*`, `skavethief_`, `Zerobeast_` | mixed; sample before use |
| `xylem_gardoom*`, `avalondragon_*`, `nievelion_anger_management_*`, `hg3300_pheaglegryph*`, `lunarkeys_rubskunk*` | non-canine stories |

### 3.D Filename pattern cheat-sheet (staged blackrat/)
Top clusters by count: `LadiesNight-`(40), `NotFreyaDragonbgs_`(25), `American*`(25), `Pokehaus-`(21), `Trexification_`(20), `Beastgurl*`(19+), `skavethief_`(19), `Deer*`(18), `alteredmom-wuf_`(14), `wolfknux_p`(11), `werewolfboy_`(10), `adoptawuff_p`(9), `weretails_page_`(9), `turned_up_to_`(9), `americanwerehog_`(9), `jet_the_wolf__page_`(9), `rub*` / fox / wuff series scattered.

---

## 4. Reusable stage vocabulary → Jack 8-frame pipeline

| Stage word | Visual cues (from packs) | Jack frame | Mismatch notes |
|---|---|---|---|
| **onset / fingertip black** | nails darken, claw tip, heat | 2 | J starts from statue contact — Fel = **no touch prop** |
| **ear migrate** | round→pointed, climb skull | 2–3 | keep short at first |
| **tee tension** | horizontal stress lines, chest dome | 3–4 | purple only |
| **muscle surge** | delts/pecs/abs pop | 4 | female breast fill concurrent |
| **tail bud** | seat-seam rip, thin then thicken | 4–5 | Anubis thin/tapered not bushy wolf |
| **sneaker burst** | toe claw punch, sole split, sock shred | 4–6 | keep Jack sneaker design |
| **crotch/shorts irreversible** | seam blowout | **5** | source often **jeans** → remap to **khaki shorts** |
| **genital rewrite** | knot/erect → shrink → vulva | **5–6** | J4 clearest |
| **muzzle push** | nose forward, jaw lengthen, fang show | **7** | avoid full feral snarl as end |
| **digitigrade** | heel rise, paw pads | 6–8 | end bipedal digitigrade stand |
| **quad drop** | all-fours arch | optional beat in **7 kneel only** | Black-rat overuses feral — constrain |
| **endform power** | bipedal flex/crouch, nude | **8** | strip gold; prefer matte short black fur + blue eyes; blonde hair remnant OK |

### Texture vocabulary
- Prefer: `short sleek black fur, soft matte, subtle rim light, tan muzzle bridge`
- Avoid from refs: `latex sheen, rubber skin, wet vinyl, polished obsidian body, oily specular over whole torso`

---

## 5. Clothes mapping (Jack lock)

| Source garment | Appears in | Map to Jack | Damage pattern to keep |
|---|---|---|---|
| Purple tee | D*, J*, (some BR) | **purple short-sleeve tee** | chest horizontal shred → straps/scraps between breasts; sleeves tear at delts |
| Khaki / tan pants | D* | **khaki shorts** (not long pants) | thigh/crotch stress → strap rags on thighs; shorter length = earlier total fail |
| Blue jeans | J*, tanraak_*, many BR | **do not draw jeans** — translate tears to khaki shorts | horizontal thigh tears, seat rip for tail, crotch blowout |
| Red/white sneakers | D5, J2/J5/J6, rubwulf, werefox | **Jack sneakers** | claw through toe box; sole split; sock shreds as white strands |
| Navy/other tees (BR) | TF_comic_BlackRat etc. | color→purple | vertical chest shred strips |
| Gloves/boots (Sonic sheets) | werehog* | N/A unless adding accessories | POP mechanics only |

**Residual cloth rule (frames 6–7):** purple scraps + khaki strap fragments clinging; frame 8 **nude** (matches project lock).

---

## 6. Do-not-copy list

1. **Wrong end species:** blue/green dragons (`tanraak_*`, D endforms), fox stockings, hedgehog/werehog IP, panther/feline, deer, bunny, T-rex, skunk, gryphon, Lombax, chipmunk-Sally.
2. **Latex-only / rubber body:** `latexshiftingvixen*`, Illustration latex-black full-body shine, D13–14 black latex dragon top.
3. **Jewelry / Egyptian gold:** forehead medallion, ear gold ribs, collar, armbands, wrist cuffs (J7–J10, Illustrations) — Fel **金饰全去**.
4. **Trigger props Fel banned:** touching Anubis statue (J1), egg touch as required beat (D1) — wardrobe/TF cues OK, prop-touch not in Jack page 2.
5. **Prolonged feral/quad pages** as sequence spine — Black-rat heavy; Jack allows only brief kneel (frame 7).
6. **Male-only endings** for Jack pipeline endform (tanraak_4–9, werefox male end, werewolfboy) — harvest mid stages only.
7. **Post-TF sex digressions** (D13–D14) — out of scope for 8-frame TF deliverable.
8. **Glasses late:** fall/skew mid-TF OK; do not keep glasses on finished Anubis unless explicitly asked.
9. **Blue jeans / cargo long pants** as Jack wardrobe.
10. **Eye color drift** to orange/yellow on final Anubis — prefer Jack **blue**.

---

## 7. Suggested prompt tag banks (copy-paste)

**POS mid-TF (frame 4-ish):**  
`1boy transforming into female anubis, messy blonde hair, blue eyes, black-rimmed glasses slipping, purple t-shirt stretching and tearing across chest, khaki shorts straining at crotch and thighs, sneakers bulging, short black fur spreading on forearms, pointed ears rising, claws forming, distressed expression, full body`

**POS clothes destruction detail:**  
`fabric stress lines, horizontal shreds, seam bursting, purple cloth strips, khaki fabric straps around thighs, sneaker toe box torn open, claw punch-through, white sock shreds, discarded fabric scraps`

**POS late (frame 7–8):**  
`female anubis, bipedal, digitigrade paws, elongated muzzle, black short fur, tan muzzle marking, large breasts, muscular abs, blonde hair remnant, blue eyes, torn purple and khaki remnants OR nude, no jewelry, no gold`

**NEG:**  
`jeans, latex, rubber skin, shiny vinyl, gold jewelry, collar, armband, forehead gem, dragon, scales, wings, hedgehog, Sonic, fox, panther, feral on all fours (except brief kneel), male only endform`

---

## 8. Analysis coverage / failures

| Item | Status |
|---|---|
| Tanraak 39 listed + staged | OK |
| Tanraak CopyToBox | OK all 39 on box |
| Tanraak vision | OK; large J3–J10 via downscaled `_preview_*` (J3 raw Read hit memory limit once; preview OK) |
| Black-rat full 1051 individual Reads | **Not done** (impractical); **17/17 contact sheets** visioned; filename taxonomy done |
| Black-rat originals >20MB | **Skipped** at staging (~55) |
| bmp in Black-rat | Skipped per jpg/png rule |
| GitHub commit | **Needs CloudAgent** (no inline create-file; `gh` unauthenticated on box) — path target below |
| Project store copy | see deposit path |

**Repo target path:** `comfyUI/furry/refs/REF_TF_Tanraak_BlackRat_knowledge.md`  
**Thin README:** `comfyUI/furry/refs/README.md`  
Prior furry assets landed via Cursor Agent PR/co-author on master (`492e008` Add comfyUI/furry…). Prefer same: CloudAgent direct push or PR to `master`.

---

## 9. Executive TF lessons (10 bullets)

1. **Best wardrobe-destruction refs are Tanraak D1–D8 + J2–J6** — purple tee + footwear burst; remap all jeans→khaki shorts.  
2. **Best Anubis species/endform refs are J5–J10 + Illustrations** — then **strip all gold** and dial latex sheen down to short matte fur.  
3. **Genital rewrite beat is clearest on J4** (knot/erect → vulva through torn crotch) → Jack frames 5–6.  
4. **Sneaker destruction grammar:** claw through toe → sole split → sock shred strands (D5, J2, J6, rubwulf, werefox).  
5. **Shirt fails at chest horizontal stress first**, then becomes hanging straps/scraps (J3, D, rubwulf).  
6. **Digitigrade = heel lift + pad reveal**, not instant monster feet (werewolfboy / AlteredGirl pad studies).  
7. **Black-rat is a mechanics encyclopedia**, not a species bible — harvest burst/pad/muzzle timing; discard IP and wrong taxa.  
8. **Jack trigger must stay prop-touch-free** even though J1/D1 are touch-triggered stories.  
9. **Quad/feral is over-represented** in Black-rat; constrain to one kneel beat so end stays bipedal female Anubis.  
10. **Do-not-copy trio that pollutes gens:** latex body, gold Egyptian jewelry, dragon/Sonic endings.

---

*Generated by Grok Bot analysis pass 2026-11-02 HKT. Adult furry TF content intentional for FelXu Jack project.*
