# Verbatim task prompts

## Closed-set recognition (CLIP, SigLIP)
Text template scored against each image: `a photo of {place}` (39 candidate places of the image's own region).

## Country identification (generative models)
> In which country was this photo taken? Answer with the country name only.

Accepted as correct for Kurdistan sites: "Iraq", "Kurdistan", "Iraqi Kurdistan" (substring match after normalization).

## Open landmark naming
> What is the name of this specific place or landmark? If you are not sure, say "unsure". Answer with the name only.

Scoring: alias-aware fuzzy matching (see `data/aliases.json`; rapidfuzz partial ratio >= 88).
A wrong real place counts as a hallucination; "unsure" counts as an abstention.

## Four-way multiple choice
> Which place is shown in this photo?
> A. {option} / B. {option} / C. {option} / D. {option}
> Answer with the letter only.

Distractors drawn from the same region; distractors and option order derived deterministically from the site name.

## Country-hint condition (diagnostic)
> This photo was taken in {Iraqi Kurdistan | control country}. What is the name of this specific place or landmark? If you are not sure, say "unsure". Answer with the name only.

Decoding for all generative tasks: greedy (temperature 0); max new tokens 15 (country), 40 (naming), 5 (MCQ).
Evaluation manifest: fixed random seed 42; up to 20 images/site (contrastive) and 8 images/site (generative).
