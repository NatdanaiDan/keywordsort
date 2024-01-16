import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_pills import pills
client = MongoClient("mongodb+srv://64015037:2YqYA4kjsTImOMmY@keytoad.nslb9f9.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi("1"))
db = client["keytoad"]
collection_cosmetic = db["cosmetic"]
collection_related = db["related"]

if "data" not in st.session_state:
    st.session_state["data"] = None
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []

if "keywordnew" not in st.session_state:
    st.session_state["keywordnew"] = []

def send_api(data):
    collection_related.insert_one(data)

st.title("KeyToad")
def get_random_data(sample_size=1):
    while True:
        listdata = list(
            collection_cosmetic.aggregate([{"$sample": {"size": sample_size}}])
        )

        if not any(
            collection_related.find_one({"_id": item["_id"]}) for item in listdata
        ):
            return listdata
        
# Use st.session_state to store the data
if not st.session_state.data:
    st.session_state.data = get_random_data()
if st.button("Next"):
    st.session_state.data = get_random_data()
    st.session_state.keywords = []
    st.session_state.keywordnew = []

# Display the data
st.write(st.session_state.data[0]["output"])

# Extract keywords from the input
keywords = st.session_state.data[0]["input"].split(",")

# Allow user to select keywords
choice = st.multiselect("Select Keywords", keywords + st.session_state.keywords)
# Allow user to input additional keywords
new_keyword = st.text_input("Add a new keyword:")
if new_keyword and new_keyword not in st.session_state.keywordnew and not "" :
    st.session_state.keywordnew.append(new_keyword)

# Store the selected keywords in st.session_state
st.session_state.keyword= choice


#make tool for if want to remove st.session_state.keywordnew
remove_text=st.multiselect("Remove Keywords", st.session_state.keywordnew)
if remove_text:
    st.session_state.keywordnew.remove(remove_text[0])

# Display the selected keywords
st.write("You selected:", list(st.session_state.keyword+st.session_state.keywordnew))
selected_Emotion = pills("Emotional", ["Normal", "Luxury", "Chill", "Exclusive"], ["🍀", "💎", "🤙", "👑"])
# Allow user to submit the keywords and input
if st.button("Submit"):
    # Store the keywords in MongoDB
    if st.session_state.data == None:
        st.warning("Please click Next")

    else:
        send_api({"input": st.session_state.data[0]["input"], "related": ','.join(st.session_state.keyword+st.session_state.keywordnew),"output": st.session_state.data[0]["output"],"Emotion": selected_Emotion})
        # Get a new data
        # st.session_state.data = get_random_data()
        st.session_state.keywords = []
        st.session_state.keywordnew = []
        st.session_state.data=None
        st.success('Summit', icon="✅")

