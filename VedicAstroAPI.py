@app.post("/get_all_horoscope_data")
async def get_chart_data(input: ChartInput):
    """ Generates all data for a given time and location, based on the selected ayanamsa & house system """
    horoscope = VedicAstro.VedicHoroscopeData(
        input.year, input.month, input.day, input.hour, input.minute,
        input.second, input.utc, input.latitude, input.longitude,
        input.ayanamsa, input.house_system
    )
    chart = horoscope.generate_chart()
    planets_data = horoscope.get_planets_data_from_chart(chart)
    houses_data = horoscope.get_houses_data_from_chart(chart)
    planet_significators = horoscope.get_planet_wise_significators(planets_data, houses_data)
    planetary_aspects = horoscope.get_planetary_aspects(chart)
    house_significators = horoscope.get_house_wise_significators(planets_data, houses_data)
    vimshottari_dasa_table = horoscope.compute_vimshottari_dasa(chart)
    consolidated_chart_data = horoscope.get_consolidated_chart_data(planets_data=planets_data, houses_data=houses_data, return_style=input.return_style)

    # Include birth time in IST and ayanamsa value in the response
    birth_time_ist = f"{input.hour + 5}:{input.minute} IST"  # Adjust for IST (UTC+5:30)

    # Calculate Krishnamurti Ayanamsa for the relevant day
    krishnamurti_ayanamsa = VedicAstro.calculate_ayanamsa(input.year, input.month, input.day, "Krishnamurti")

    return {
        "birth_time_ist": birth_time_ist,
        "ayanamsa": input.ayanamsa,
        "krishnamurti_ayanamsa": krishnamurti_ayanamsa,
        "planets_data": [planet._asdict() for planet in planets_data],
        "houses_data": [house._asdict() for house in houses_data],
        "planet_significators": planet_significators,
        "planetary_aspects": planetary_aspects,
        "house_significators": house_significators,
        "vimshottari_dasa_table": vimshottari_dasa_table,
        "consolidated_chart_data": consolidated_chart_data
    }
