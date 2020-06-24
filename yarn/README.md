Acquired using the following links: (Account at yarn(dot)co and authenticated cookies required)

```
https://yarn.co/api/interactions?noCache=true&team_id=16&video_id=187245
https://yarn.co/api/interactions?noCache=true&team_id=16&video_id=187246
https://yarn.co/api/interactions?noCache=true&team_id=16&video_id=187247
```

interaction_type: "transcript" seems to be required for some reason

To acquire a video link from an object:

```json
{
"id": 870247,
"video_id": 187245,
"interaction_type": "transcript",
"transcript": "Tkk-tkk-tkk-tkk-tkk-tkk-tkk! Yousa cannot bees hair.",
"start_time": 893.534,
"end_time": 897.996,
"clip_url": "10fc8b46-4846-46b7-a9a2-6d020a24088b.mp4",
"thumb_url": "10fc8b46-4846-46b7-a9a2-6d020a24088b_thumb.jpg",
"uuid": "10fc8b46-4846-46b7-a9a2-6d020a24088b",
"created_at": "2015-11-17T07:12:07.000Z",
"updated_at": "2017-05-29T19:27:45.000Z",
"Video": 187245
}
```
Yarn website:
- `https://www.getyarn.io/yarn-clip/${thumb_url}`

Raw mp4:
- `https://y.yarn.co/${clip_url}`

Small thumbnail:
- `https://y.yarn.co/${thumb_url}`

Large thumbnail
- `https://y.yarn.co/${uuid}_screenshot.jpg`

Reddit share link:
- `http://www.reddit.com/submit?url=${url}`
