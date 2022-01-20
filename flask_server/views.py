from flask import Blueprint, render_template, request, send_file
from services.utils import (
    get_random_quote,
    get_increment_and_save_n_button_clicks,
    get_image_from_bucket,
)

views = Blueprint('views', __name__)

n_button_clicks = 0

@views.route('/', methods=['GET', 'POST'])
def home():
    n_button_clicks = get_increment_and_save_n_button_clicks(
        increment=request.method == 'POST'
    )
    image_from_gcs = get_image_from_bucket()
    return render_template(
        'index.html',
        n_button_clicks=n_button_clicks,
        random_quote=get_random_quote(),
    )


@views.route('/image')
def image():
    return send_file(get_image_from_bucket(), download_name='logo2.png')
