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
    message.add(content())

    # Social media icons for use in the about dialog
    icon_linkedin = resources_path('img', 'icons', 'about', 'svg', 'linkedin.svg')
    icon_twitter = resources_path('img', 'icons', 'about', 'svg', 'twitter.svg')

    # Adds the icons to the about dialog
    message.add(tr(
        '<div class="col-4">'
        '<div class="pull-right">'
        '<p class="text-center"> Connect with us </p>'
        '<ul class="nav  justify-content-center">'
        '<li class="px-2">'
        '<li class="px-2"> <a href="https://x.com/earthdailya">'
        f'<img src={resource_url(icon_twitter)} height=35 width=35 >'
        '</a></li>'
        '<li class="px-2"> <a href="https://www.linkedin.com/company/earthdailyanalytics">'
        f'<img src={resource_url(icon_linkedin)} height=35 width=35 /></li>'
        '<a/></li>'
        '</ul>'
        '</div>'
        '</div>'
        '</div>'
    )
    )

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
        '<h3><a id="None"> </a> About EarthDaily </h3>'
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
        '<li>'
        '<span class="hint">EarthDaily </span><b> is a global leader in Earth observation '
        'delivering unparalleled geospatial insights across industries such as Agriculture, water management, and forest planning. '
        'With a team of world-class agronomists, data scientists, and Earth observation specialists, '
        'EarthDaily transforms the highest-quality satellite imagery into actionable solutions.'
        '</li>'
        '<li class="message">By combining advanced analytics and superior signal-to-noise ratio data, '
        'EarthDaily empowers organizations to mitigate risk, optimize operations, and achieve sustainable outcomes. '
        "Explore how EarthDaily's innovative platforms support the vital sectors shaping our world at "
        '<a class="links" href="https://earthdaily.com/"> earthdaily.com</a></b>'
        '</li> '
        '</ul>'
        '</div>'
    )))

    return message
