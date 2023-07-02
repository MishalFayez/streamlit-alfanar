import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    menu_items= {
        'About':
        """
        # Hello
        ## Thank you for trying the app
        """
    }
    

)
css='''
[data-testid="stSidebarNav"] {
    position:absolute;
    bottom: 0;
    color: white !important;
}
.css-j7qwjs {
    color: white !important;
}
'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.sidebar.image("new.png")
st.markdown("""
<style>
[data-testid=stSidebar] {
  background-color: #2d5d9f;
  color: white !important;
}
</style>
""", unsafe_allow_html=True)



st.sidebar.markdown("# <span style='color:white'>Sales Analytic</span> ", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )



if __name__ == "__main__":
    get_UN_data()
    st.write(st.experimental_user)