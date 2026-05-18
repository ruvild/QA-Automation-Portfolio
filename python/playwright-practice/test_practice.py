from playwright.sync_api import Page, expect
import re
import os
import pytest


def test_ab(page: Page):
    page.goto('https://the-internet.herokuapp.com/abtest')
    header = page.get_by_role('heading', level=3)
    expect(header).to_be_visible()
    expect(header).to_contain_text('A/B Test')


def test_add_remove_elements(page: Page):
    page.goto('https://the-internet.herokuapp.com/add_remove_elements/')
    add_button = page.get_by_role('button', name='Add Element')
    delete_button = page.get_by_role('button', name='Delete')
    add_button.click(click_count=5)
    expect(delete_button).to_have_count(5)
    delete_button.nth(2).click()
    expect(delete_button).to_have_count(4)


def test_basic_auth(page: Page):
    page.goto('https://admin:admin@the-internet.herokuapp.com/basic_auth')
    text_locator = page.locator('.example')
    expect(text_locator).to_contain_text(
        'Congratulations! You must have the proper credentials.'
    )


def test_broken_images(page: Page):
    page.goto('https://the-internet.herokuapp.com/broken_images')
    images = page.locator('.example').get_by_role('img')
    broken_count = 0
    for image in range(images.count()):
        is_broken = images.nth(image).evaluate(
            "(element) => element.naturalWidth === 0"
        )
        if is_broken:
            broken_count += 1
    assert broken_count == 2, f"Expected 2 broken images, but found {broken_count}."


def test_calendar(page: Page):
    page.goto('https://practice-automation.com/calendars/')
    page.get_by_text('Select or enter a date').click()
    page.get_by_role('button', name='Next Month').click(click_count=2)
    page.get_by_role('button', name='15').click()
    expect(page.get_by_role('textbox', name='You are currently')).to_have_value(
        '2026-07-15'
    )


def test_challenging_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/challenging_dom')
    edit_button = (
        page.locator('tr').filter(has_text='Iuvaret9').get_by_role('link', name='edit')
    )
    edit_button.click()
    expect(page).to_have_url(re.compile(r'.*#edit'))


def test_checkboxes(page: Page):
    page.goto('https://the-internet.herokuapp.com/checkboxes')

    checkbox_1 = page.get_by_role('checkbox').nth(0)
    checkbox_2 = page.get_by_role('checkbox').nth(1)
    checkbox_1.check()
    checkbox_2.uncheck()
    expect(checkbox_1).to_be_checked()
    expect(checkbox_2).not_to_be_checked()


def test_checkboxes_xpath(page: Page):
    page.goto('https://testautomationpractice.blogspot.com/')
    checkboxes = page.locator("//label[text()='Days:']//parent::div").get_by_role(
        'checkbox'
    )
    expect(checkboxes).to_have_count(7)
    for i in range(checkboxes.count()):
        expect(checkboxes.nth(i)).not_to_be_checked()


def test_context_menu(page: Page):

    page.goto('https://the-internet.herokuapp.com/context_menu')
    page.on('dialog', lambda dialog: dialog.accept())
    page.locator('#hot-spot').click(button='right')
    selenium_link = page.get_by_role('link', name='Elemental Selenium')
    expect(selenium_link).to_be_enabled()


def test_digest_auth(page: Page):
    page.goto('https://admin:admin@the-internet.herokuapp.com/digest_auth')
    text_locator = page.locator('.example')
    expect(text_locator).to_contain_text(
        'Congratulations! You must have the proper credentials.'
    )


def test_disappearing_elements(page: Page):
    page.goto('https://the-internet.herokuapp.com/disappearing_elements')
    for _ in range(5):
        try:
            page.get_by_role('link', name='Gallery').click(timeout=2000)
            print(f"Found the button on try {_}")
            break
        except:
            page.reload()
    expect(page).to_have_url('https://the-internet.herokuapp.com/gallery/')


def test_drag_n_drop(page: Page):
    page.goto('https://the-internet.herokuapp.com/drag_and_drop')
    square_a = page.locator('#column-a')
    square_b = page.locator('#column-b')
    square_a.drag_to(square_b)
    expect(square_a.locator('header')).to_have_text('B')
    expect(square_b.locator('header')).to_have_text('A')


def test_dropdown(page: Page):
    page.goto('https://the-internet.herokuapp.com/dropdown')
    dropdown = page.locator('#dropdown')
    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value('2')


def test_dynamic_content(page: Page):
    page.goto('https://the-internet.herokuapp.com/dynamic_content')
    row = page.locator('#content .row').first
    old_text = row.inner_text()
    page.reload()
    expect(row).not_to_have_text(old_text)


def test_dynamic_waiting(page: Page):
    page.goto('https://the-internet.herokuapp.com/dynamic_controls')
    checkbox = page.get_by_role('checkbox')
    page.get_by_role('button', name='Remove').click()
    expect(page.locator('#loading')).to_be_hidden()
    expect(page.locator('#message')).to_have_text("It's gone!")
    expect(checkbox).to_be_hidden()
    textbox = page.get_by_role('textbox')
    page.get_by_role('button', name='Enable').click()
    expect(textbox).to_be_enabled()


def test_dynamic_loading(page: Page):
    page.goto('https://the-internet.herokuapp.com/dynamic_loading/2')
    page.get_by_role('button', name='Start').click()
    expect(page.get_by_role('heading', level=4)).to_be_visible()


def test_entry_ad(page: Page):
    page.goto('https://the-internet.herokuapp.com/entry_ad')
    modal = page.locator('#modal')
    expect(modal).to_be_visible()
    modal.get_by_text('Close').click()
    expect(modal).to_be_hidden()


def test_exit_intent(page: Page):
    page.goto('https://the-internet.herokuapp.com/exit_intent')
    page.mouse.move(100, 100)
    page.mouse.move(100, -10)
    modal = page.locator('#ouibounce-modal')
    expect(modal).to_be_visible()
    modal.get_by_text('Close').click()
    expect(modal).to_be_hidden()


def test_file_donwload(page: Page):
    page.goto('https://the-internet.herokuapp.com/download')
    file_path = "C:/Users/Admin/Documents/mypy/playwright/gems"
    with page.expect_download() as download_info:
        page.get_by_text('some-file.txt').click()
    download = download_info.value
    download.save_as(os.path.join(file_path, download.suggested_filename))
    assert os.path.isfile(os.path.join(file_path, download.suggested_filename))


def test_file_upload(page: Page):
    page.goto('https://the-internet.herokuapp.com/upload')
    page.set_input_files(
        'input[id=file-upload]',
        'C:/Users/Admin/Documents/mypy/playwright/gems/some-file.txt',
    )
    page.get_by_role('button', name='upload').click()
    expect(page.get_by_text('File Uploaded!')).to_be_visible()


def test_floating_menu(page: Page):
    page.goto('https://the-internet.herokuapp.com/floating_menu')
    page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
    expect(page.get_by_role('link', name='Home')).to_be_visible()


def test_forgot_password(page: Page):
    page.goto('https://the-internet.herokuapp.com/forgot_password')
    page.get_by_label('E-mail').fill('test_best_abc@mymail.com')
    with page.expect_request('**/forgot_password') as request_info:
        page.get_by_role('button', name='Retrieve password').click()
    request = request_info.value
    assert "forgot_password" in request.url
    assert request.method == "POST"


def test_login(page: Page):
    page.goto('https://the-internet.herokuapp.com/login')
    page.get_by_label('Username').fill('tomsmith')
    page.get_by_label('Password').fill('SuperSecretPassword!')
    with page.expect_response('**secure') as response_info:
        page.get_by_role('button', name=' Login').click()
    response = response_info.value
    expect(page).to_have_url(re.compile(r'.*/secure'))
    assert response.status == 200


def test_frames(page: Page):
    page.goto('https://the-internet.herokuapp.com/frames')
    page.get_by_role('link', name='Nested Frames').click()
    middle_frame = (
        page.frame_locator("frame[name='frame-top']")
        .frame_locator("frame[name='frame-middle']")
        .locator('body')
    )
    expect(middle_frame).to_have_text('MIDDLE')


def test_iframe_pw(page: Page):
    page.goto('https://practice-automation.com/iframes/')
    frame = page.frame_locator('iframe#iframe-1')
    frame.get_by_role('link', name='Docs').click()
    expect(frame.get_by_role('heading', level=1)).to_have_text('Installation')


def test_iframes(page: Page):
    page.goto('https://the-internet.herokuapp.com/iframe')
    textbox = page.frame_locator('#mce_0_ifr').locator('body#tinymce')
    try:
        textbox.fill('Test')
    except TimeoutError:
        print('The action timed out: Element might not be interactable or found.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')  # This captures the "Why"


def test_geolocation(page: Page):
    latitude = 48.8584
    longitude = 2.2945
    page.goto('https://the-internet.herokuapp.com/geolocation')
    page.context.grant_permissions(['geolocation'])
    page.context.set_geolocation({"latitude": latitude, "longitude": longitude})
    page.get_by_role('button', name='Where am I?').click()

    expect(page.locator('#lat-value')).to_contain_text(str(latitude))
    expect(page.locator('#long-value')).to_contain_text(str(longitude))


def test_horizontal_slider(page: Page):
    page.goto('https://the-internet.herokuapp.com/horizontal_slider')
    slider = page.locator("input[type='range']")
    slider.focus()
    slider_value = 0
    while slider_value < 4.5:
        old_slider_value = slider_value
        slider.press('ArrowRight')
        slider_value = float(page.locator('#range').inner_text())
        if old_slider_value == slider_value:
            print(f'Max slider value is {old_slider_value}')
            break
    assert slider_value == 4.5


def test_hovers(page: Page):
    page.goto('https://the-internet.herokuapp.com/hovers')
    first_image = page.locator('#content .figure').first
    first_image.hover()
    expect(first_image.get_by_role('heading')).to_be_visible()
    expect(first_image.get_by_role('link')).to_be_visible()


def test_infinite_scroll(page: Page):
    page.goto('https://the-internet.herokuapp.com/infinite_scroll')
    paragraph = page.locator('.jscroll-added')
    target_count = 5
    while paragraph.count() < target_count:
        page.mouse.wheel(0, 1000)
    try:
        expect(paragraph).to_have_count(paragraph.count() + 1, timeout=2000)
    except AssertionError:
        # If it didn't load, try one more nudge
        page.mouse.wheel(0, 500)

    assert paragraph.count() >= target_count


def test_inputs(page: Page):
    page.goto('https://the-internet.herokuapp.com/inputs')
    input_field = page.locator("input[type='number']")
    input_field.type('123')
    input_field.type('abc')
    expect(input_field).to_have_value('123')
    up_key_presses = 5
    for _ in range(up_key_presses):
        input_field.press('ArrowUp')

    expect(input_field).to_have_value(str(123 + up_key_presses))


def test_jquery(page: Page):
    page.goto('https://the-internet.herokuapp.com/jqueryui/menu')
    file_path = "C:/Users/Admin/Documents/mypy/playwright/gems"
    page.get_by_role('link', name='Enabled').hover()
    page.get_by_text('Downloads').hover()
    with page.expect_download() as download_info:
        page.get_by_text('Excel').click()
    download = download_info.value
    download.save_as(os.path.join(file_path, download.suggested_filename))
    assert os.path.isfile(os.path.join(file_path, download.suggested_filename))


def test_js_alerts(page: Page):
    page.goto('https://the-internet.herokuapp.com/javascript_alerts')
    page.goto('https://the-internet.herokuapp.com/javascript_alerts')
    page.once('dialog', lambda dialog: dialog.accept())
    page.get_by_text('Click for JS Alert').click()
    page.once('dialog', lambda dialog: dialog.dismiss())
    page.get_by_text('Click for JS Confirm').click()
    page.once('dialog', lambda dialog: dialog.accept('arara'))
    page.get_by_text('Click for JS prompt').click()
    expect(page.locator('#result')).to_contain_text('arara')


def test_JS_error(page: Page):
    with page.expect_event('pageerror') as error_info:
        page.goto('https://the-internet.herokuapp.com/javascript_error')
    error = error_info.value.message
    assert "xyz" in error


def test_key_presses(page: Page):
    page.goto('https://the-internet.herokuapp.com/key_presses')
    textbox = page.get_by_role('textbox')
    key_regular = 'A'
    key_special = 'Tab'
    key_combo = 'Control'
    textbox.press(key_regular)
    expect(page.locator('#result')).to_have_text(
        re.compile(f'You entered: {key_regular}', re.IGNORECASE)
    )
    textbox.press(key_special)
    expect(page.locator('#result')).to_have_text(
        re.compile(f'You entered: {key_special}', re.IGNORECASE)
    )
    textbox.press(key_combo)
    expect(page.locator('#result')).to_have_text(
        re.compile(f'You entered: {key_combo}', re.IGNORECASE)
    )


def test_large_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/large')
    row = page.locator('#large-table').get_by_role('row').filter(has_text='27.1')
    cell = row.get_by_role('cell').nth(4)
    expect(cell).to_have_text('27.5')
    expect(page.locator('#siblings div').last).to_contain_text('50')


def test_large_dom_xpath(page: Page):
    page.goto('https://the-internet.herokuapp.com/large')
    cell = page.locator("//td[text()='50.1']")
    cell_sibling = cell.locator('//following-sibling::td[1]')
    expect(cell_sibling).to_have_text('50.2')
    # locator('..') works as well
    parent_row = cell_sibling.locator('//ancestor::tr[1]')
    expect(parent_row).to_have_class('row-50')


def test_modals(page: Page):
    page.goto('https://practice-automation.com/modals/')
    page.get_by_role('button', name='Simple Modal').click()
    modal = page.get_by_role('dialog')
    expect(modal).to_contain_text("Hi, I’m a simple modal.")
    modal.get_by_role('button', name='Close').click()


def test_multiple_windows(page: Page):
    page.goto('https://the-internet.herokuapp.com/windows')
    with page.context.expect_page() as new_page_info:
        page.get_by_role('link', name='Click Here').click()
    new_page = new_page_info.value
    expect(new_page.get_by_role("heading")).to_contain_text('New Window')
    new_page.close()
    expect(page.get_by_role('link', name='Elemental Selenium')).to_be_visible()


def test_notification_message(page: Page):
    page.goto('https://the-internet.herokuapp.com/notification_message_rendered')
    notification = page.locator('#flash')
    reload_link = page.get_by_role('link', name='Click here')
    for _ in range(10):
        reload_link.click()
        content = notification.text_content()
        if content and 'Action successful' in content:
            break
    expect(notification).to_contain_text('Action successful')


def test_pagination(page: Page):

    def change_pagination_and_verify(page: Page, amount: str, expected_count: int):
        # 1. The Action
        paginator = page.get_by_label(' entries per page')
        paginator.select_option(amount)

        # 2. The Verification (DRYing up the repetitive expects)
        table_rows = page.locator('table#tablepress-1 tbody tr')
        footer = page.get_by_role('status').filter(has_text='Showing')

        expect(table_rows).to_have_count(expected_count)
        expect(footer).to_contain_text(f"1 to {expected_count} of")

    page.goto('https://practice-automation.com/tables/')
    # Initial check
    expect(page.locator('table#tablepress-1 tbody tr')).to_have_count(10)
    # Use the helper to scale up
    change_pagination_and_verify(page, '25', 25)


def test_redirection(page: Page):
    page.goto('https://the-internet.herokuapp.com/redirector')
    page.get_by_role('link', name='here').click()
    expect(page).to_have_url(re.compile(r'.*status_codes'))
    expect(page.get_by_role('heading', level=3)).to_contain_text('Status Codes')


def test_secure_file_download(page: Page):
    page.goto('https://admin:admin@the-internet.herokuapp.com/download_secure')
    file_path = "C:/Users/Admin/Documents/mypy/playwright/gems"
    with page.expect_download() as download_info:
        page.get_by_role('link', name='test.txt', exact=True).click()
    download = download_info.value
    download.save_as(os.path.join(file_path, download.suggested_filename))
    assert os.path.isfile(os.path.join(file_path, download.suggested_filename))


def test_shadow_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/shadowdom')
    expect(
        page.locator('span').filter(has_text="Let's have some different text!")
    ).to_be_visible()


def test_shifting_content(page: Page):
    page.goto('https://the-internet.herokuapp.com/shifting_content/menu')
    page.get_by_role('link', name='Gallery').click()
    expect(page).to_have_url(re.compile(r'.*/gallery'))


def test_slow_resources(page: Page):
    with page.expect_response('**slow_external', timeout=40000) as slow_request_info:
        page.goto('https://the-internet.herokuapp.com/slow')
    slow_request = slow_request_info.value
    assert slow_request.status == 503


def test_sortable_tables(page: Page):

    def _get_column():
        return page.locator('table#table1 tbody tr td:nth-child(1)').all_inner_texts()

    page.goto('https://the-internet.herokuapp.com/tables')
    unsorted_last_name = _get_column()
    manually_sorted = sorted(unsorted_last_name)
    # Wait until the first cell in the body is not empty
    page.locator('table#table1 tbody tr td').first.wait_for(state="visible")
    page.locator('#table1').get_by_text('Last Name').click(force=True)
    auto_sorted = _get_column()
    assert manually_sorted == auto_sorted


def test_status_codes(page: Page):

    def _get_response(response_code):
        page.goto('https://the-internet.herokuapp.com/status_codes')
        with page.expect_response(
            lambda response: response.status == response_code
        ) as response_info:
            page.get_by_role('link', name=f'{response_code}').click()
        response = response_info.value
        assert response.status == response_code

    _get_response(404)
    _get_response(500)


def test_tooltip(page: Page):
    page.goto('https://practice-automation.com/popups/')
    tooltip = page.get_by_text("click me")
    tooltip.click()
    expect(page.locator('#myTooltip')).to_contain_text('Cool text')


def test_typos(page: Page):
    page.goto('https://the-internet.herokuapp.com/typos')
    for _ in range(10):
        expect(page.locator('#content p').last).to_contain_text("Sometimes")
        page.reload()
