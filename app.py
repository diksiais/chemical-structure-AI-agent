import streamlit as st
from chemical_lookup import fetch_pubchem_image
from paper_search import search_papers
from database import save_chemical

st.title("Chemical Research Agent")

chemical_input = st.text_input("Enter chemical name or CAS number:")

if st.button("Search"):
    cid, image_url, source = fetch_pubchem_image(chemical_input)
    if cid:
        st.image(image_url, caption=f"{chemical_input} (Source: {source})")
        st.success(f"CID: {cid}")
        save_chemical(chemical_input, "", cid, image_url)

        st.subheader("Related Papers")
        papers = search_papers(chemical_input)
        for p in papers:
            st.markdown(f"**{p['title']}** ({p['year']})")
            st.markdown(f"[Read more]({p['url']})")
            st.markdown(p.get('abstract', 'No abstract available'))
            st.markdown("---")
    else:
        st.error("Chemical not found.")
