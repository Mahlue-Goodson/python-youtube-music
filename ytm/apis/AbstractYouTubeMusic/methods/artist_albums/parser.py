from ... import utils

__all__ = __name__.split('.')[-1:]

def parse(data):
    contents = utils.get_nested \
    (
        data,
        'contents',
        'singleColumnBrowseResultsRenderer',
        'tabs',
        0,
        'tabRenderer',
        'content',
        'sectionListRenderer',
        'contents',
        0,
        'musicShelfRenderer',
        'contents',
    )

    albums_data = []

    for item in contents:
        item = utils.get_nested \
        (
            item,
            'musicResponsiveListItemRenderer',
        )

        item_menu_items = utils.get_nested \
        (
            item,
            'menu',
            'menuRenderer',
            'items',
            default = (),
        )

        item_menu_items_map = {}

        for item_menu_item in item_menu_items:
            item_menu_item = utils.first_key(item_menu_item)

            item_menu_item_text = utils.get_nested \
            (
                item_menu_item,
                'text',
                'runs',
                0,
                'text',
            )

            if not item_menu_item_text:
                item_menu_item_text = utils.get_nested \
                (
                    item_menu_item,
                    'defaultText',
                    'runs',
                    0,
                    'text',
                )

            if not item_menu_item_text:
                return # raise

            # Change this to use camel-case, then update the extractors
            item_menu_item_identifier = item_menu_item_text.strip().lower().replace(' ', '_')

            item_menu_items_map[item_menu_item_identifier] = item_menu_item

        item_badges = utils.get_nested \
        (
            item,
            'badges',
            default = (),
        )

        item_badges_map = {}

        for badge in item_badges:
            badge = utils.first_key(badge)

            badge_label = utils.get_nested \
            (
                badge,
                'accessibilityData',
                'accessibilityData',
                'label',
            )

            if not badge_label:
                return # raise/log

            badge_identifier = badge_label.strip().lower().replace(' ', '_')

            item_badges_map[badge_identifier] = badge

        item_browse_endpoint = utils.get_nested \
        (
            item,
            'navigationEndpoint',
            'browseEndpoint',
        )
        item_shuffle_playlist_endpoint = utils.get_nested \
        (
            item_menu_items_map,
            'shuffle_play',
            'navigationEndpoint',
            'watchPlaylistEndpoint',
        )
        item_radio_playlist_endpoint = utils.get_nested \
        (
            item_menu_items_map,
            'start_radio',
            'navigationEndpoint',
            'watchPlaylistEndpoint',
        )
        item_flex_column_0_runs = utils.get_nested \
        (
            item,
            'flexColumns',
            0,
            'musicResponsiveListItemFlexColumnRenderer',
            'text',
            'runs',
        )
        item_flex_column_1_runs = utils.get_nested \
        (
            item,
            'flexColumns',
            1,
            'musicResponsiveListItemFlexColumnRenderer',
            'text',
            'runs',
        )

        item_album_page_type = utils.get_nested \
        (
            item_browse_endpoint,
            'browseEndpointContextSupportedConfigs',
            'browseEndpointContextMusicConfig',
            'pageType',
        )
        item_thumbnail = utils.get_nested \
        (
            item,
            'thumbnail',
            'musicThumbnailRenderer',
            'thumbnail',
            'thumbnails',
            -1,
        )
        item_album_id = utils.get_nested \
        (
            item_browse_endpoint,
            'browseId',
        )
        item_album_params = utils.get_nested \
        (
            item_browse_endpoint,
            'params',
        )
        item_album_name = utils.get_nested \
        (
            item_flex_column_0_runs,
            0,
            'text',
        )
        item_type = utils.get_nested \
        (
            item_flex_column_1_runs,
            0,
            'text',
        )
        item_year = utils.get_nested \
        (
            item_flex_column_1_runs,
            2,
            'text',
            func = int,
        )
        item_shuffle_playlist_params = utils.get_nested \
        (
            item_shuffle_playlist_endpoint,
            'params',
        )
        item_shuffle_playlist_id = utils.get_nested \
        (
            item_shuffle_playlist_endpoint,
            'playlistId',
        )
        item_radio_playlist_params = utils.get_nested \
        (
            item_radio_playlist_endpoint,
            'params',
        )
        item_radio_playlist_id = utils.get_nested \
        (
            item_radio_playlist_endpoint,
            'playlistId',
        )
        item_explicit = 'explicit' in item_badges_map

        item_data = \
        {
            'name':      item_album_name,
            'id':        item_album_id,
            'type':      item_type,
            'year':      item_year,
            'explicit':  item_explicit,
            'params':    item_album_params,
            'thumbnail': item_thumbnail,
            'shuffle': \
            {
                'params':      item_shuffle_playlist_params,
                'playlist_id': item_shuffle_playlist_id,
            },
            'radio': \
            {
                'params':      item_radio_playlist_params,
                'playlist_id': item_radio_playlist_id,
            },
        }

        albums_data.append(item_data)

    return albums_data
