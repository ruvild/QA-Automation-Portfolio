from selene import be, have


def test_images(saby_main):

    saby_contacts = saby_main.go_to_contacts_via_header()
    tensor_main = saby_contacts.go_to_tensor()
    tensor_main.switch_to_next_tab()
    tensor_main.people_block.should(be.visible)
    tensor_about = tensor_main.go_to_about_page()
    tensor_about.browser.should(have.url_containing(tensor_about.url))
    tensor_about.working_block_images.should(be.visible)
    first_image_dimensions = tensor_about.first_image_dimensions
    assert all(
        image.locate().size == first_image_dimensions
        for image in tensor_about.working_block_images
    )
