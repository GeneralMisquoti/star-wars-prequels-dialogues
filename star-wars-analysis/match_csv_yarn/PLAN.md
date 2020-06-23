# PLAN
1. For each csv row:
   1. Look for matches fuzzily in range [previous_id..] inclusive.
      1. Sort by order.
         1. Choose first match. (What if no match?)
            1. If no match, print.
      2. Just use the first match.
   3. If previous match's id is different from the current, set previous
      to be the current.
2. Fix rest by hand, but not do all by hand!
      
### Problems

#### 1. Problem: CSV larger than JSON

```csv
NUTE,MAOI MADAKOR,6,"Yes, of course. As you know, our blockade is perfectly legal...",4,16,870087;870088
```

```json
[{
  "id": 870087,
  "video_id": 187245,
  "interaction_type": "transcript",
  "transcript": "Yes, of course.",
  "start_time": 131.148,
  "end_time": 133.065,
  "clip_url": "e42a28b2-7977-4de2-8f4b-3a3f10ead148.mp4",
  "thumb_url": "e42a28b2-7977-4de2-8f4b-3a3f10ead148_thumb.jpg",
  "uuid": "e42a28b2-7977-4de2-8f4b-3a3f10ead148",
  "created_at": "2015-11-17T07:11:04.000Z",
  "updated_at": "2017-05-29T19:25:18.000Z",
  "Video": 187245
},
{
  "id": 870088,
  "video_id": 187245,
  "interaction_type": "transcript",
  "transcript": "As you know, our blockade is perfectly legal,",
  "start_time": 133.15,
  "end_time": 136.277,
  "clip_url": "18a419d7-e49c-4f5f-b0c7-e7815098ae6d.mp4",
  "thumb_url": "18a419d7-e49c-4f5f-b0c7-e7815098ae6d_thumb.jpg",
  "uuid": "18a419d7-e49c-4f5f-b0c7-e7815098ae6d",
  "created_at": "2015-11-17T07:11:04.000Z",
  "updated_at": "2017-05-29T19:25:20.000Z",
  "Video": 187245
}]
```

##### Solutions:
1. Break each CSV quote by dots?
   - the speakers will be the same, since the CSV is the source of truth

#### 2. Problem: JSON larger than CSV


```csv
BATTLE DROID,NA,40,"Check it out, Corporal. We'll cover you.",1,7,
BATTLE DROID 2,NA,41,"Roger, roger.",1,2,
```

```json
{
    "id": 870135,
    "video_id": 187245,
    "interaction_type": "transcript",
    "transcript": "- Check it out, Corporal. We'll cover you. - Roger, roger.",
    "start_time": 342.525,
    "end_time": 345.486,
    "clip_url": "4b16fd43-40ed-4b35-991e-80df7366036b.mp4",
    "thumb_url": "4b16fd43-40ed-4b35-991e-80df7366036b_thumb.jpg",
    "uuid": "4b16fd43-40ed-4b35-991e-80df7366036b",
    "created_at": "2015-11-17T07:11:23.000Z",
    "updated_at": "2017-05-29T19:25:58.000Z",
    "Video": 187245
}
```

##### Solutions
1. Using the previous ID thing should fix this.
