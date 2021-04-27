from aiogram import types

import config
from searcher import searcher


class MemesExtension:
    @staticmethod
    def get_inline_results(inline_query):
        items = []
        memes = searcher.get_memes()
        offset = int(inline_query.offset or 0)

        for meme in memes[offset:offset + config.MAX_INLINE_RESULTS]:
            result_id = str(hash(meme['link']))

            item = types.InlineQueryResultPhoto(
                id=result_id,
                photo_url=meme["link"],
                thumb_url=meme["link"]
            )
            items.append(item)

        next_offset = str(offset + config.MAX_INLINE_RESULTS) if len(items) == config.MAX_INLINE_RESULTS else ""
        return items, next_offset


extensions = {
    "memes": MemesExtension
}
