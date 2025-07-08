import streamlit as st

main_page = st.Page(
    page ='pages/Turkey_main.py',
    title='National Waste Dashboard',
)

province_page = st.Page(
    page ='pages/Provinces_main.py',
    title='Provincial Waste Dashboard',
)

storymaps_page = st.Page(
    page ='pages/storymaps.py',
    title='Storymaps',
)



# Navication setup with sections
pg = st.navigation(

    {
        "Dashboard": [main_page, province_page],
        "Story Maps": [storymaps_page]
    }
)

pg.run()

