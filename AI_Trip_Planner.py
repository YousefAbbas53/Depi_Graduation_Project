import streamlit as st
from openai import OpenAI
import datetime

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

st.title("AI Travel Planner 🌍")

with st.form("travel_form"):
    starting_point = st.text_input("Starting Point (City or Landmark)", placeholder="E.g., New York")
    destinations = st.text_input("Destination (City or Landmark) with comma separated", placeholder="E.g., Paris, London, Rome")
    starting_date = st.date_input("Starting Date", min_value=datetime.date.today())
    ending_date = st.date_input("Ending Date", min_value=starting_date)
    num_travelers = st.number_input("Number of Travelers", min_value=1, value=1)
    currency = st.selectbox("Currency", options=["USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CNY"])
    budget = st.number_input("Budget", min_value=500)
    trip_type = st.selectbox("Trip Type", options=["Adventure", "Leisure", "Cultural", "Romantic", "Family", "Solo", "Budget"])
    submit_btn = st.form_submit_button("Get Travel Plan", type="primary")

if submit_btn:
    if not all([starting_point, destinations, starting_date, ending_date, currency, budget, trip_type]):
        st.error("Please fill all the fields")
    else:
        with st.spinner("Generating your AI travel plan..."):
            prompt = f"""
            Create a detailed daily travel itinerary with the following information:

            Starting from: {starting_point}
            Destinations to visit: {destinations}
            Trip start from {starting_date} to {ending_date}
            Number of travelers: {num_travelers}
            Budget: {budget} {currency}
            Travel style: {trip_type}

            Please provide a day-by-day itinerary including:
            1. Transportation options between locations
            2. Recommended accommodations
            3. Key attractions to visit each day
            4. Estimated costs for each major activity
            5. Local cuisine recommendations
            6. Any practical tips or considerations

            Format the response in a clear, organized manner with sections for each day.
            """

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are an AI travel planner."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.write(response.choices[0].message.content) 