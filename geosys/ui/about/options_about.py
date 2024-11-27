# coding=utf-8
"""About text for options dialog."""

import os
from geosys import messaging as m
from geosys.messaging import styles
from geosys.utilities.i18n import tr
from geosys.utilities.resources import resources_path, resource_url

SUBSECTION_STYLE = styles.SUBSECTION_LEVEL_3_STYLE
INFO_STYLE = styles.BLUE_LEVEL_4_STYLE
SMALL_ICON_STYLE = styles.SMALL_ICON_STYLE

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'


def options_about():
    """About message for options dialog.

    .. versionadded:: 3.2.1

    :returns: A message object containing information for the about dialog.
    :rtype: messaging.message.Message
    """

    message = m.Message()
    message.add(heading())
    
    # Social media icons for use in the about dialog
    icon_linkedin = resources_path('img', 'icons', 'about', 'svg', 'linkedin.svg')
    icon_twitter = resources_path('img', 'icons', 'about', 'svg', 'twitter.svg')
    icon_youtube = resources_path('img', 'icons', 'about', 'svg', 'youtube.svg')
    # Use a table for layout with updated icon placement and padding
    message.add(tr(
        '<table style="width: 100%; border-spacing: 10px;">'
        '<tr>'
        # Left Section: Main Content
        '<td style="vertical-align: top; text-align: left; width: 70%; padding-right: 20px; padding-left: 0;">'
        f'{content().to_html()}'
        '</td>'
        # Right Section: Social Media Icons
        '<td style="vertical-align: top; text-align: center; width: 30%;">'
        '<p><strong>Connect with us</strong></p>'
        '<table style="margin: 10px auto; border-spacing: 30px;">'
        '<tr>'
        f'<td><a href="https://twitter.com/EarthDailyAgro/">'
        f'<img src={resource_url(icon_twitter)} height=35 width=35 alt="Twitter"></a></td>'
        f'<td><a href="https://www.linkedin.com/company/115836/admin/">'
        f'<img src={resource_url(icon_linkedin)} height=35 width=35 alt="LinkedIn"></a></td>'
        f'<td><a href="https://www.youtube.com/channel/UCy4X-hM2xRK3oyC_xYKSG_g">'
        f'<img src={resource_url(icon_youtube)} height=35 width=35 alt="YouTube"></a></td>'
        '</tr>'
        '</table>'
        '</td>'
        '</tr>'
        '</table>'
    ))


    return message


def heading():
    """Method that returns just the header.

    This method was added so that the text could be reused in the
    other contexts.

    .. versionadded:: 3.2.2

    :returns: A heading object.
    :rtype: geosys.messaging.heading.Heading
    """
    heading_message = tr(
        '<div class="row subsection">'
        '<div>'
        '<h3><a id="None"> </a> About EarthDaily Agro </h3>'
        '</div>'
        '</div>'
    )
    return heading_message


def content():
    """Method that returns just the content.

    This method was added so that the text could be reused.

    .. versionadded:: 3.2.2

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    message = m.Message()
    message.add(m.Paragraph(tr(
        '<div class="row">'
        '<div class="col-8">'
        '<ul class="list-unstyled">'
        '<p>'
        '<span class="hint">EarthDaily Agro</span><b> is the agricultural analysis division '
        'of EarthDaily Analytics. '
        'Learn more about EarthDaily at '
        '<a class="links" href="https://earthdailyagro.com/"> earthdaily.com</a></b>'
        '</p>'
        '<p class="message">EarthDaily Agro uses satellite imaging to provide '
        'advanced analytics to mitigate risk and the planet. '
        'Increase efficiencies - leading to more sustainable '
        'outcomes for the organization and people who '
        'feed.</p> '
        '</ul>'
        '</div>'
    )))

    return message
