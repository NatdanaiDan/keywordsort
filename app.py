import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_pills import pills

client = MongoClient(
    "mongodb+srv://64015037:2YqYA4kjsTImOMmY@keytoad.nslb9f9.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi("1"),
)
db = client["keytoad"]
collection_cosmetic = db["test"]
collection_related = db["mode_human"]
old_values = [0, 1, 2, 3, 4]


def send_api(data):
    collection_related.insert_many(data)


st.title("KeyToad")


def get_random_data(sample_size=5):
    while True:
        listdata = list(
            collection_cosmetic.aggregate([{"$sample": {"size": sample_size}}])
        )

        if not any(
            collection_related.find_one({"_id": item["_id"]}) for item in listdata
        ):
            return listdata


if "data" not in st.session_state:
    st.session_state.data = get_random_data()

if "listemo" not in st.session_state:
    st.session_state.listemo = [None, None, None, None, None]

# Use st.session_state to store the data
# if not st.session_state.data:
#     st.session_state.data = get_random_data()
if st.button("Next"):
    st.session_state.data = get_random_data()

# Display the data
if st.session_state.data:
    for i in range(5):
        st.write(
            st.session_state.data[i]["input"],
        )
        value = st.selectbox(
            "Emotion", ["Normal", "Luxury", "Chill", "Exclusive"], key=i
        )
        st.session_state.listemo[i] = value

    # Allow user to submit the keywords and input
    if st.button("Submit"):
        # Store the keywords in MongoDB
        if st.session_state.data == None:
            st.warning("Please click Next")

        else:
            # print(st.session_state.data)
            # send_api(st.session_state.listemo)
            listdata = []
            for i in range(5):
                listdata.append(
                    {
                        "input": st.session_state.data[i]["input"],
                        "Emotion": st.session_state.listemo[i],
                        "output": st.session_state.data[i]["output"],
                    }
                )
            send_api(listdata)
            st.session_state.listemo = [None, None, None, None, None]
            # send_api()
            # Get a new data
            # st.session_state.data = get_random_data()
            # st.write("You selected:", {"input": st.session_state.data[0]["input"], "related": ','.join(st.session_state.keyword+st.session_state.keywordnew),"output": st.session_state.data[0]["output"],"Emotion": selected_Emotion})

            st.session_state.data = None
            st.success("Summit", icon="✅")
