import streamlit as st
import replicate
import os
from transformers import AutoTokenizer

# Set assistant icon to Snowflake logo
icons = {"assistant": "./Snowflake_Logomark_blue.svg", "user": "⛷️"}

# App title
st.set_page_config(page_title="World Travel App")

# Replicate Credentials
with st.sidebar:
    st.title('World Travel App')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your Replicate API token.', icon='⚠️')
            st.markdown("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")

    os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. I'll teach you about the world. Ask me anything."}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. I'll teach you about the world. Ask me anything."}]

@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text
    text to the Model. Eventually we will replace this with ArcticTokenizer
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)

# Function for generating Snowflake Arctic response
def generate_arctic_response(prompt_str):
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.button('Clear chat history', on_click=clear_chat_history, key="clear_chat_history")
        st.stop()

    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}",
                                  }):
        yield str(event)

# User-provided prompt through chat input
user_input = st.chat_input(placeholder="Type your additional question here...", disabled=not replicate_api)

# Function to handle both chat input and button click
def handle_user_input(input_text):
    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        with st.chat_message("user", avatar="⛷️"):
            st.write(input_text)
        
        prompt = []
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                prompt.append("user\n" + dict_message["content"] + "")
            else:
                prompt.append("assistant\n" + dict_message["content"] + "")
        
        prompt.append("assistant")
        prompt.append("")
        prompt_str = "\n".join(prompt)
        
        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant", avatar="./Snowflake_Logomark_blue.svg"):
                response = generate_arctic_response(prompt_str)
                full_response = st.write_stream(response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)

region_country_dict = {
    "Africa":[
        "Burundi",
        "Comoros",
        "Djibouti",
        "Eritrea",
        "Ethiopia",
        "Kenya",
        "Madagascar",
        "Malawi",
        "Mauritius",
        "Mayotte",
        "Mozambique",
        "Reunion",
        "Rwanda",
        "Seychelles",
        "Somalia",
        "Tanzania, United Republic of",
        "Uganda",
        "Zambia",
        "Zimbabwe",
        "Angola",
        "Cameroon",
        "Central African Republic",
        "Chad",
        "Congo (Brazzaville)",
        "Congo, Democratic Republic of the",
        "Equatorial Guinea",
        "Gabon",
        "Sao Tome and Principe",
        "Algeria",
        "Egypt",
        "Libyan Arab Jamahiriya",
        "Morroco",
        "South Sudan",
        "Sudan",
        "Tunisia",
        "Western Sahara",
        "Botswana",
        "Eswatini (ex-Swaziland)",
        "Lesotho",
        "Namibia",
        "South Africa",
        "Benin",
        "Burkina Faso",
        "Cape Verde",
        "Cote d'Ivoire (Ivory Coast)",
        "Gambia",
        "Ghana",
        "Guinea",
        "Guinea-Bissau",
        "Liberia",
        "Mali",
        "Mauritania",
        "Niger",
        "Nigeria",
        "Saint Helena",
        "Senegal",
        "Sierra Leone",
        "Togo",
    ],
    "Asia":[
        "Afghanistan",
        "Armenia",
        "Azerbaijan",
        "Bangladesh",
        "Bhutan",
        "Brunei Darussalam",
        "Cambodia",
        "China",
        "Georgia",
        "Hong Kong",
        "India",
        "Indonesia",
        "Japan",
        "Kazakhstan",
        "Korea, North",
        "Korea, South",
        "Kyrgyzstan",
        "Laos",
        "Macao",
        "Malaysia",
        "Maldives",
        "Mongolia",
        "Myanmar (ex-Burma)",
        "Nepal",
        "Pakistan",
        "Philippines",
        "Singapore",
        "Sri Lanka (ex-Ceilan)",
        "Taiwan",
        "Tajikistan",
        "Thailand",
        "Timor Leste (West)",
        "Turkmenistan",
        "Uzbekistan",
        "Vietnam",
    ],
    "Europe":[
        "Austria",
        "Belgium",
        "Bulgaria",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Albania",
        "Andorra",
        "Belarus",
        "Bosnia",
        "Croatia",
        "European Union",
        "Faroe Islands",
        "Gibraltar",
        "Guernsey and Alderney",
        "Iceland",
        "Isle of Man",
        "Jersey",
        "Kosovo",
        "Liechtenstein",
        "Moldova",
        "Monaco",
        "Montenegro",
        "North Macedonia",
        "Norway",
        "Russia",
        "San Marino",
        "Serbia",
        "Svalbard and Jan Mayen Islands",
        "Switzerland",
        "Turkey",
        "Ukraine",
        "United Kingdom",
        "Vatican City State (Holy See)",
    ],
    "Middle East":[
        "Bahrain",
        "Iraq",
        "Iran",
        "Israel",
        "Jordan",
        "Kuwait",
        "Lebanon",
        "Oman",
        "Palestine",
        "Qatar",
        "Saudi Arabia",
        "Syria",
        "United Arab Emirates",
        "Yemen",
    ],
    "Oceania":[
        "Australia",
        "Fiji",
        "French Polynesia",
        "Guam",
        "Kiribati",
        "Marshall Islands",
        "Micronesia",
        "New Caledonia",
        "New Zealand",
        "Papua New Guinea",
        "Samoa",
        "Samoa, American",
        "Solomon, Islands",
        "Tonga",
        "Vanuatu",
    ],
    "The Americas":[
        "Bermuda",
        "Canada",
        "Greenland",
        "Saint Pierre and Miquelon",
        "United States",
        "Belize",
        "Costa Rica",
        "El Salvador",
        "Guatemala",
        "Honduras",
        "Mexico",
        "Nicaragua",
        "Panama",
        "Anguilla",
        "Antigua and Barbuda",
        "Aruba",
        "Bahamas",
        "Barbados",
        "Bonaire, Saint Eustatius and Saba",
        "British Virgin Islands",
        "Cayman Islands",
        "Cuba",
        "Curaçao",
        "Dominica",
        "Dominican Republic",
        "Grenada",
        "Guadeloupe",
        "Haiti",
        "Jamaica",
        "Martinique",
        "Monserrat",
        "Puerto Rico",
        "Saint-Barthélemy",
        "St. Kitts and Nevis",
        "Saint Lucia",
        "Saint Martin",
        "Saint Vincent and the Grenadines",
        "Sint Maarten",
        "Trinidad and Tobago",
        "Turks and Caicos Islands",
        "Virgin Islands (US)",
        "Argentina",
        "Bolivia",
        "Brazil",
        "Chile",
        "Colombia",
        "Ecuador",
        "Falkland Islands (Malvinas)",
        "French Guiana",
        "Guyana",
        "Paraguay",
        "Peru",
        "Suriname",
        "Uruguay",
        "Venezuela",
    ],
}

st.sidebar.button('Clear chat history', on_click=clear_chat_history, type="primary")

region = st.sidebar.selectbox(
   "Select Region (optional)",
   list(region_country_dict),
   index=None,
   placeholder="type/search region",
)

country = st.sidebar.selectbox(
   "Select Country (required)",
   region_country_dict[region] if region else sum(list(region_country_dict.values()), []),
   index=None,
   placeholder="type/search country",
)

if country and st.sidebar.button(f'Learn about {country} :memo:'):
    on_click=handle_user_input(f"Tell me about {country}.")

if country and st.sidebar.button(f'Plan a itinerary in {country} :airplane:'):
    on_click=handle_user_input(f"Suggest 1 week itinerary in {country}, output as table.")

if user_input:
    handle_user_input(user_input)

st.sidebar.subheader("About")
st.sidebar.caption("This app makes you feel like traveling around the world, using [Snowflake Arctic](https://www.snowflake.com/blog/arctic-open-and-efficient-foundation-language-models-snowflake) model. App hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Model hosted by [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct).")
