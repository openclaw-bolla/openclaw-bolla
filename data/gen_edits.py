import json

en = json.load(open('/home/bolla/workspace/data/ki_buch_en_adapted.json'))

# Each edit: (chapter_index, old, new, category, reason)
E = []
def add(idx, old, new, cat, reason):
    E.append({"chapter_index": idx, "old": old, "new": new, "category": cat, "reason": reason})

# ---------------- CH12 ----------------
# Maria/separation/grief: thirty -> twenty-two. Keep instinct(30), Guenter(40), marriage(32), project(12).
add(12, "Brought back.\" He looked at her — thirty years of distrust and a love he had never been able",
        "Brought back.\" He looked at her — twenty-two years of distrust and a love he had never been able",
        "grief", "distrust/love over the separation = 22 (DE: zweiundzwanzig Jahre Misstrauen)")
add(12, "you were gone one morning without a word. Thirty years, Maria. And I never understood it.",
        "you were gone one morning without a word. Twenty-two years, Maria. And I never understood it.",
        "separation", "since she left = 22 (DE: Zweiundzwanzig Jahre, Maria)")
add(12, "asked something he had been forbidding himself for thirty years.",
        "asked something he had been forbidding himself for twenty-two years.",
        "grief", "question forbidden since she left = 22")
add(12, "a grief, so old and so deep that thirty years had done nothing to change it",
        "a grief, so old and so deep that twenty-two years had done nothing to change it",
        "grief", "old grief = 22")
add(12, "a gesture that was twenty years old. \"Don't ask me any more",
        "a gesture that was twenty-two years old. \"Don't ask me any more",
        "grief", "gesture as old as the separation = 22 (DE: zweiundzwanzig Jahre alt)")
# Keep [6] instinct 30, [7] Guenter 40, [8] marriage 32 unchanged.

# ---------------- CH15 ----------------
# Keep [5] "I've known Maria for thirty years" (30). Convert [6][7][8][9][10] 30->22.
add(15, "without a word, and for thirty years I believed she had betrayed me",
        "without a word, and for twenty-two years I believed she had betrayed me",
        "grief", "belief held since she left = 22")
add(15, "I spent thirty years hating a man I never saw",
        "I spent twenty-two years hating a man I never saw",
        "grief", "hatred since she left = 22")
add(15, "For thirty years I thought I'd taken it from her",
        "For twenty-two years I thought I'd taken it from her",
        "grief", "guilt held since she left = 22")
add(15, "an old pain that had lasted thirty years",
        "an old pain that had lasted twenty-two years",
        "grief", "old pain = 22")
add(15, "You, because you've needed to know for thirty years.",
        "You, because you've needed to know for twenty-two years.",
        "grief", "needing to know since she left = 22")

# ---------------- CH17 ----------------
# Prose rewrite of the math beat (positions [2..6]) + scattered grief 30->22.
add(17,
    "\"Twenty-two years,\" he said, his voice rough. \"She left me — left me thirty years ago. Without a word. And eight years later\" — he did the math, right in front of her, and his hand trembled over the paper — \"eight years later she founds a foundation for someone named Aurora and stays silent about it to this day.\" He looked up, and in his eyes sat an old, familiar pain in the process of turning into something worse. \"So there really was someone. For thirty years I told myself I'd only imagined him. And now he has a name.\"",
    "\"Twenty-two years,\" he said, his voice rough. \"She left me — left me twenty-two years ago. Without a word.\" — he did the math, right in front of her, and his hand trembled over the paper — \"The same year she left, she founds a foundation for someone named Aurora and stays silent about it to this day.\" He looked up, and in his eyes sat an old, familiar pain in the process of turning into something worse. \"So there really was someone. For twenty-two years I told myself I'd only imagined him. And now he has a name.\"",
    "rewrite", "Math beat reworded so separation and foundation both fall 22 years ago (matches DE: 'Im selben Jahr, in dem sie ging, legt sie eine Stiftung an'). Removes the thirty/eight-years-later arithmetic.")
# [7] "guarding the wrong one for thirty years" -> 22 (regret since she left)
add(17, "And I just realized that for thirty years I've been guarding the wrong one — my own.",
        "And I just realized that for twenty-two years I've been guarding the wrong one — my own.",
        "grief", "guarding the wrong grave since she left = 22")
# [10] "thirty years ago you walked away from me" -> 22
add(17, "into the ground for her. And thirty years ago you walked away from me without a single",
        "into the ground for her. And twenty-two years ago you walked away from me without a single",
        "separation", "walked away = 22")
# [12][13] "Thirty years, Maria... Thirty years I reached out every morning" -> 22
add(17, "\"Thirty years, Maria,\" he said softly. \"Thirty years I reached out every morning to the empty side",
        "\"Twenty-two years, Maria,\" he said softly. \"Twenty-two years I reached out every morning to the empty side",
        "grief", "reaching out every morning since she left = 22")
# [15] "Thirty years I've been jealous of a dead man" -> 22
add(17, "no joy in it. \"Thirty years I've been jealous of a dead man.",
        "no joy in it. \"Twenty-two years I've been jealous of a dead man.",
        "grief", "jealousy since she left = 22")
# Keep [3]=in rewrite, [8]? Let's verify the remaining 30 in ch17 is instinct. [14][16] are forty (instinct) - keep.

# ---------------- CH23 ----------------  Noah bug: ten -> fifteen
add(23, "a stone in the foundation that I didn't set. That someone set before me. Ten years before I was even here.",
        "a stone in the foundation that I didn't set. That someone set before me. Fifteen years before I was even here.",
        "noah", "Noah came 12 years ago; the earlier marker must be MORE than 12 -> fifteen (DE: vor fünfzehn Jahren, bevor ich überhaupt da war)")

# ---------------- CH25 ---------------- [0] twenty -> twenty-two (sealed room since loss)
add(25, "the reflex of a man who had spent twenty years learning to function in exactly these moment",
        "the reflex of a man who had spent twenty-two years learning to function in exactly these moment",
        "grief", "functioning since the loss = 22 (DE: zweiundzwanzig Jahre)")

# ---------------- CH28 ---------------- all three twenty -> twenty-two
add(28, "I don't sound soft. I haven't sounded soft in twenty years.\"",
        "I don't sound soft. I haven't sounded soft in twenty-two years.\"",
        "grief", "not soft since the loss = 22")
add(28, "the voice he had used long ago, twenty years ago, in a different city, in a different lif",
        "the voice he had used long ago, twenty-two years ago, in a different city, in a different lif",
        "grief", "long ago = 22")
add(28, "Because despite everything, despite twenty years, he believed this one thing she was telling",
        "Because despite everything, despite twenty-two years, he believed this one thing she was telling",
        "grief", "despite the years apart = 22")

# ---------------- CH29 ---------------- [2] twenty -> twenty-two (Maria eating men for breakfast)
add(29, "a woman who had been eating men like Kern for breakfast for twenty years.",
        "a woman who had been eating men like Kern for breakfast for twenty-two years.",
        "grief", "Maria's span = 22 (DE: zweiundzwanzig Jahre)")

# ---------------- CH30 ---------------- [2] twenty -> twenty-two (wall that held)
add(30, "a crack in a wall that had held for twenty years.",
        "a crack in a wall that had held for twenty-two years.",
        "grief", "wall that held since the loss = 22")

# ---------------- CH31 ----------------
# DE=[12,20,22,22,22,30,22,2,22,12,22] EN=[12,20,30,30,30,30,20,2,22,12,20]
# Convert EN [2][3][4] 30->22, [6] 20->22, [10] 20->22. Keep [5]=30 (service), [1]=20 stays(20)? DE[1]=20 keep.
add(31, "but inside his own head, buried thirty years deep and carefully sealed over.",
        "but inside his own head, buried twenty-two years deep and carefully sealed over.",
        "grief", "buried memory since the loss = 22")
add(31, "in a room he had avoided for thirty years, in a city he had never returned to",
        "in a room he had avoided for twenty-two years, in a city he had never returned to",
        "grief", "room avoided since the loss = 22")
add(31, "But this time it came back. For the first time in thirty years, the thought came back after Theo had cut it",
        "But this time it came back. For the first time in twenty-two years, the thought came back after Theo had cut it",
        "grief", "first time in the years since the loss = 22")
# [5] "anything he had seen in thirty years of service" -> KEEP (service)
add(31, "she had been dreading this moment for twenty years.",
        "she had been dreading this moment for twenty-two years.",
        "grief", "Maria dreading the reveal since the loss = 22")
add(31, "who had not cried in front of anyone in twenty years — not in front of Director Howell",
        "who had not cried in front of anyone in twenty-two years — not in front of Director Howell",
        "grief", "not cried since the loss = 22")

# ---------------- CH32 ----------------
# DE=[22,22,22,2m,40,22,22,22,30,22,30] EN=[22,22,20,2m,40,20,22,30,30,30,30,22]
# EN has 12 items vs DE 11 -> EN has an extra 30. Map: [2]20->22, [5]20->22. Keep service 30s.
add(32, "Maria had been putting that mask on for twenty years. It fit better than her own face.",
        "Maria had been putting that mask on for twenty-two years. It fit better than her own face.",
        "grief", "mask worn since the loss = 22")
add(32, "thought about Maria, who had been bleeding for twenty years over something she'd never shown anyone",
        "thought about Maria, who had been bleeding for twenty-two years over something she'd never shown anyone",
        "grief", "bleeding since the loss = 22")
# [7..10] are service/avoidance 30s; DE has one 30 at [8] (service) and one at [10] (room avoided->but DE[10]? )
# Per DE, position of "room he'd been avoiding for thirty years" -> DE? CH32 DE has dreißig at [8] and [10].
# EN [7] "avoiding for thirty years" = the room -> DE shows zweiundzwanzig? Re-check below in verify.

# ---------------- CH33 ---------------- [6] twenty -> twenty-two (something a woman doesn't sell for)
add(33, "Something a woman doesn't sell for twenty years.",
        "Something a woman doesn't sell for twenty-two years.",
        "grief", "value she wouldn't sell = 22 (DE: zweiundzwanzig Jahre)")

# ---------------- CH34 ----------------
# Prose double removal + grief 20->22
add(34, "even Maria Santos, who hadn't taken orders from anyone in twenty years.",
        "even Maria Santos, who hadn't taken orders from anyone in twenty-two years.",
        "grief", "Maria's span = 22")
add(34, "completely, and the twenty years and the twenty-two years and the number that had never added up right",
        "completely, and the twenty-two years and the number that had never added up right",
        "rewrite", "Remove the 'twenty years and twenty-two years' double (DE collapsed to just zweiundzwanzig Jahre)")
add(34, "to something she has been waiting twenty years to reach",
        "to something she has been waiting twenty-two years to reach",
        "grief", "waiting since the loss = 22")
add(34, "to read the one thing she had spent twenty years praying she would never have to hear",
        "to read the one thing she had spent twenty-two years praying she would never have to hear",
        "grief", "dreading to hear since the loss = 22")

# ---------------- CH35 ----------------
# DE=[20,22,20,22,4,7m,4,7m,22,2,22,22,22] EN=[20,20,20,20,6,4m,6,4m,20,20,20,20,20]
# [0]=20 keep(DE 20). [1]20->22. [2]=20 keep. [3]20->22. deathage 6->4 & 4m->7m (x2). [8..12] 20->22 (but [9]=DE2? )
# Re-examine: DE[9]=2 (zwei Jahr). EN[9]=20. That is a mismatch in alignment; verify in script.
add(35, "I haven't heard it in twenty years. Nobody says it anymore.",
        "I haven't heard it in twenty-two years. Nobody says it anymore.",
        "grief", "name unheard since the loss = 22")
add(35, "she had opened a floodgate that had been sealed for twenty years. \"Born on the fourteenth of March.",
        "she had opened a floodgate that had been sealed for twenty-two years. \"Born on the fourteenth of March.",
        "grief", "floodgate sealed since the loss = 22")
# deathage
add(35, "\"— died at six years and four months. Of something that could have been caught",
        "\"— died at four years and seven months. Of something that could have been caught",
        "deathage", "daughter died at four years and seven months (DE canon)")
add(35, "every tantrum and every laugh. Six years and four months, in data.",
        "every tantrum and every laugh. Four years and seven months, in data.",
        "deathage", "four years and seven months of recorded life (DE canon)")
add(35, "just a statement that had taken twenty years to arrive.",
        "just a statement that had taken twenty-two years to arrive.",
        "grief", "statement = 22")
add(35, "at a bedside that had come twenty years too late.",
        "at a bedside that had come twenty-two years too late.",
        "grief", "too late by 22")
add(35, "and then I've spent twenty years trying to comfort a dead machine",
        "and then I've spent twenty-two years trying to comfort a dead machine",
        "grief", "comforting since the loss = 22")
add(35, "as final as everything you've put off for twenty years too long.",
        "as final as everything you've put off for twenty-two years too long.",
        "grief", "put off for 22")
add(35, "the name of a child who had died twenty years ago.",
        "the name of a child who had died twenty-two years ago.",
        "grief", "child died 22 years ago")

# ---------------- CH36 ---------------- all three twenty -> twenty-two
add(36, "You don't understand. *I* didn't understand it for twenty years.\"",
        "You don't understand. *I* didn't understand it for twenty-two years.\"",
        "grief", "not understood for 22")
add(36, "the way no one has looked at me in twenty years",
        "the way no one has looked at me in twenty-two years",
        "grief", "no one looked at her like that in 22")
add(36, "a face that had just aged twenty years all at once.",
        "a face that had just aged twenty-two years all at once.",
        "grief", "aged 22 at once")

# ---------------- CH37 ----------------
# DE=[4,22,22,22,6,6,22,6,22,22] EN=[4,20,20,20,6,6,20,20,20]
# EN has 9, DE 10. Project=4 keep. cradle=6 keep. grief 20->22: [1][2][3][6][7][8].
add(37, "watching the man she had loved and lost twenty years ago and hated and loved and hated ever since",
        "watching the man she had loved and lost twenty-two years ago and hated and loved and hated ever since",
        "grief", "loved and lost 22 years ago")
add(37, "between them the whole distance of twenty years, which suddenly didn't feel like hostility",
        "between them the whole distance of twenty-two years, which suddenly didn't feel like hostility",
        "grief", "distance of 22 years")
add(37, "something was running between them on a frequency twenty years old that nobody else could receive",
        "something was running between them on a frequency twenty-two years old that nobody else could receive",
        "grief", "frequency 22 years old")
add(37, "for the first time in twenty years. \"I never put away the cradle.",
        "for the first time in twenty-two years. \"I never put away the cradle.",
        "grief", "breathing through for first time in 22")
add(37, "the man who for twenty years had been unable to come home, because home w",
        "the man who for twenty-two years had been unable to come home, because home w",
        "grief", "unable to come home for 22")
add(37, "a voice that was suddenly no longer twenty years old, but young and full of terror",
        "a voice that was suddenly no longer twenty-two years old, but young and full of terror",
        "grief", "voice no longer 22 years old")

# ---------------- CH38 ----------------
# DE=[6,6,6,6,6,22,22,6,6,22,6,6,6,22,6,6,6,22] EN ends with 6 at last instead of 22.
# Convert the 'twenty years' (grief) ones: EN [5][6][9][13] are 'twenty', plus the final DE 22 EN has as ?? .
# EN twenty positions: [5]='six years deep and twenty years deeper', [6]='spent twenty years not saying', [9]='took twenty years off his face', [13]='on his way to this door for twenty years'
add(38, "something six years deep and twenty years deeper.",
        "something six years deep and twenty-two years deeper.",
        "grief", "22 years deeper than the 6-year cradle")
add(38, "Yes, I do. I've spent twenty years not saying things out loud",
        "Yes, I do. I've spent twenty-two years not saying things out loud",
        "grief", "silent for 22")
add(38, "lit-from-within smile, and it took twenty years off his face.",
        "lit-from-within smile, and it took twenty-two years off his face.",
        "grief", "took 22 years off his face")
add(38, "the footsteps of a man who had been on his way to this door for twenty years without knowing it.",
        "the footsteps of a man who had been on his way to this door for twenty-two years without knowing it.",
        "grief", "on his way for 22")

# ---------------- CH39 ----------------
# DE=[4,22,22,22,22,22,22,4,4] EN=[4,20,20,20,20,20,20,4,4]. Convert all six 'twenty' -> twenty-two.
add(39, "at a place where nothing had broken in twenty years.",
        "at a place where nothing had broken in twenty-two years.",
        "grief", "nothing broken in 22")
add(39, "kept locked in separate boxes for twenty years — each their own, each alone.",
        "kept locked in separate boxes for twenty-two years — each their own, each alone.",
        "grief", "boxed away for 22")
add(39, "crying for the first time in twenty years, quietly, without words",
        "crying for the first time in twenty-two years, quietly, without words",
        "grief", "first cry in 22")
add(39, "you wouldn't open the door for me. Twenty years, Maria. You didn't open the door for twenty years.*",
        "you wouldn't open the door for me. Twenty-two years, Maria. You didn't open the door for twenty-two years.*",
        "grief", "didn't open the door for 22 (both mentions)")
add(39, "something was healing that had been open for twenty years, and both were happening at once",
        "something was healing that had been open for twenty-two years, and both were happening at once",
        "grief", "wound open for 22")

# ---------------- CH40 ---------------- all three twenty -> twenty-two
add(40, "those steady hands had spent twenty years resting on everything in the world except",
        "those steady hands had spent twenty-two years resting on everything in the world except",
        "grief", "hands resting for 22")
add(40, "I've kept you out for twenty years. Don't let me push you away tonight.",
        "I've kept you out for twenty-two years. Don't let me push you away tonight.",
        "grief", "kept him out for 22")
add(40, "I've been standing in exactly this room for twenty years, Maria.",
        "I've been standing in exactly this room for twenty-two years, Maria.",
        "grief", "standing in this room for 22")

# ---------------- CH41 ----------------
# DE=[22,22,22,22] EN=[20,20,21,21]. Convert [0][1] 20->22, [2][3] 21->22.
add(41, "a sound she had not been allowed to make in twenty years.",
        "a sound she had not been allowed to make in twenty-two years.",
        "grief", "sound not allowed in 22")
add(41, "every photo that Maria collected over twenty years and fed into this thing.",
        "every photo that Maria collected over twenty-two years and fed into this thing.",
        "grief", "collected over 22 (DE: zweiundzwanzig Jahre)")
add(41, "And I wasn't here for twenty-one years. I don't have the right to say",
        "And I wasn't here for twenty-two years. I don't have the right to say",
        "grief", "absent for 22 (DE canon zweiundzwanzig)")
add(41, "the sound a man makes when he hasn't cried in twenty-one years and can't hold it back anymore.",
        "the sound a man makes when he hasn't cried in twenty-two years and can't hold it back anymore.",
        "grief", "hasn't cried in 22 (DE canon)")

# ---------------- CH42 ----------------
# DE=[22,22,20,22,22,4,4] EN=[21,20,20,21,22,4]. EN 6 items, DE 7. daughter age beat differs.
# [0]21->22, [1]=20 keep(DE20), [2]=20 keep? DE[2]=20. [3]21->22.
add(42, "I hadn't thought about that in twenty-one years. And now she's telling me the light goes on",
        "I hadn't thought about that in twenty-two years. And now she's telling me the light goes on",
        "grief", "hadn't thought of it in 22 (DE canon)")
add(42, "For twenty-one years I didn't have to do exactly this, and look w",
        "For twenty-two years I didn't have to do exactly this, and look w",
        "grief", "for 22 years she didn't (DE canon)")
# [4] already twenty-two. daughter age in dialogue:
add(42, "\"Theo and I. Twenty-two years ago. She made it to four. She died at four,",
        "\"Theo and I. Twenty-two years ago. She made it to four. She died at four years and seven months,",
        "deathage", "explicit death age = four years and seven months (DE canon)")

# ---------------- CH43 ----------------
# DE all 22. EN=[22,20,20,20,20]. Convert [1][2][3][4] 20->22.
add(43, "She's spent twenty years collecting everything to bring her daughter",
        "She's spent twenty-two years collecting everything to bring her daughter",
        "grief", "collecting for 22")
add(43, "with a clarity that must have been waiting underneath everything for twenty years.\n\n  \"That's what I wanted.\"",
        "with a clarity that must have been waiting underneath everything for twenty-two years.\n\n  \"That's what I wanted.\"",
        "grief", "waiting for 22")
add(43, "And I spent twenty years mourning the wrong half of it.",
        "And I spent twenty-two years mourning the wrong half of it.",
        "grief", "mourning for 22")
add(43, "A place that none of us has gone to in twenty years, because none of us could bear it.",
        "A place that none of us has gone to in twenty-two years, because none of us could bear it.",
        "grief", "unvisited for 22")

# ---------------- CH44 ----------------
# DE=[22,1,22,22,22,22,22,22,22,22] EN all twenty (9). Convert all nine 20->22.
add(44, "two dates between them that kept us both from sleeping for twenty years.",
        "two dates between them that kept us both from sleeping for twenty-two years.",
        "grief", "sleepless for 22")
add(44, "neither of us could bring ourselves to live there, and for twenty years it's been sitting empty",
        "neither of us could bring ourselves to live there, and for twenty-two years it's been sitting empty",
        "grief", "house empty for 22")
add(44, "I haven't been able to pick up the key in twenty years without feeling sick.",
        "I haven't been able to pick up the key in twenty-two years without feeling sick.",
        "grief", "key untouched for 22")
add(44, "into the room a little while ago. \"Twenty years. This whole city thinks I'm a cold woman",
        "into the room a little while ago. \"Twenty-two years. This whole city thinks I'm a cold woman",
        "grief", "22 years")
add(44, "You're moving in with her for the first time. Twenty years late. But you're moving in.",
        "You're moving in with her for the first time. Twenty-two years late. But you're moving in.",
        "grief", "22 years late")
add(44, "it was between me and my belly, twenty years ago —",
        "it was between me and my belly, twenty-two years ago —",
        "grief", "22 years ago")
add(44, "a woman throwing open a door that had been shut for twenty years. \"We're bringing her home.\"",
        "a woman throwing open a door that had been shut for twenty-two years. \"We're bringing her home.\"",
        "grief", "door shut for 22")
add(44, "Three hours to turn a house dead for twenty years into a place where a child can live.",
        "Three hours to turn a house dead for twenty-two years into a place where a child can live.",
        "grief", "house dead for 22")
add(44, "I'll open up the house. For the first time in twenty years.\"",
        "I'll open up the house. For the first time in twenty-two years.\"",
        "grief", "first time in 22")

# ---------------- CH45 ----------------
# DE=[20,22,22,22,22] EN all twenty (5). [0]=20 keep (DE 20: 'twenty years working jobs'). [1..4] 20->22.
add(45, "A house that drew thirty watts for twenty years and since last night has been eating like a",
        "A house that drew thirty watts for twenty-two years and since last night has been eating like a",
        "grief", "house drew thirty watts for 22")
add(45, "there had been a first time, twenty years ago, when a child had gone dark",
        "there had been a first time, twenty-two years ago, when a child had gone dark",
        "grief", "child went dark 22 years ago")
add(45, "about Maria who for twenty years hadn't been able to visit a grave",
        "about Maria who for twenty-two years hadn't been able to visit a grave",
        "grief", "couldn't visit grave for 22")
add(45, "the child Maria hadn't been able to bury for twenty years, riding for the first time",
        "the child Maria hadn't been able to bury for twenty-two years, riding for the first time",
        "grief", "couldn't bury for 22")

# ---------------- CH46 ----------------
# DE=[22,4,4,4,22,4,4,7m,22,22,22,22,22] EN=[20,4,4,4,20,4,4,7m,21,21,21,21,21]
# [0]20->22, [4]20->22, [8..12]21->22. four-years (project/age) keep.
add(46, "Her voice thinned. \"She waited twenty years in a corpus, Marley.",
        "Her voice thinned. \"She waited twenty-two years in a corpus, Marley.",
        "grief", "waited 22 in a corpus (DE: zweiundzwanzig)")
add(46, "Maria had what went into it — she had spent twenty years collecting what remains of a child",
        "Maria had what went into it — she had spent twenty-two years collecting what remains of a child",
        "grief", "collected for 22")
add(46, "the same gate he hadn't parked at in twenty-one years — and sat there",
        "the same gate he hadn't parked at in twenty-two years — and sat there",
        "grief", "hadn't parked there in 22 (DE canon)")
add(46, "He had kept it for twenty-one years as proof that there had been a before.",
        "He had kept it for twenty-two years as proof that there had been a before.",
        "grief", "kept key 22 years (DE canon)")
add(46, "two people who had walked in opposite directions for twenty-one years and found themselves at the same point",
        "two people who had walked in opposite directions for twenty-two years and found themselves at the same point",
        "grief", "apart for 22 (DE canon)")
add(46, "Is Theo the same man who ran away twenty-one years ago? No.",
        "Is Theo the same man who ran away twenty-two years ago? No.",
        "grief", "ran away 22 years ago (DE canon)")
add(46, "Maria, who had waited twenty-one years for that question without knowing it would e",
        "Maria, who had waited twenty-two years for that question without knowing it would e",
        "grief", "waited 22 years (DE canon)")

# ============ VERIFY ============
fails=[]
for e in E:
    idx=e["chapter_index"]; old=e["old"]
    c=en['kapitel'][idx]['text'].count(old)
    if c!=1:
        fails.append((idx, c, old[:70]))
if fails:
    print("UNIQUENESS FAILURES:")
    for f in fails: print(" ", f)
else:
    print("All %d edits have exactly one match." % len(E))

# category counts
from collections import Counter
print(Counter(e["category"] for e in E))

json.dump({"edits": E}, open('/home/bolla/workspace/data/en_timeline_edits.json','w'), ensure_ascii=False, indent=2)
print("written", len(E))
