from selene import be, have


def test_region(saby_main, region="Камчатский", url_region="kamchatskij"):
    saby_contacts = saby_main.go_to_contacts_via_footer()
    saby_contacts.region_header.should(be.visible)
    saby_contacts.partner_contacts.should(be.visible)
    saby_contacts.switch_region(region)

    saby_contacts.region_header.should(have.text(region))
    saby_contacts.partner_contacts.should(have.text(region))
    saby_contacts.browser.should(have.title_containing(region))
    saby_contacts.browser.should(have.url_containing(url_region))
