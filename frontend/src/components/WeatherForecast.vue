<!-- TODO: Add map of location -->
<template>

  <div id="weather-forecast" class="container">
    <div class="row">
      <div class="col-3 fs-2">Weather Forecast</div>
      <div class="col fs-2">{{ location.name }} ({{ location.code }}) / {{ location.country_name }}
        ({{ location.country_code }})
      </div>
    </div>
    <div class="row mt-4">
      <div class="col col-md-3">
        <div class="form-floating mb-2">
          <input v-model="search" @input="locationAutocomplete" type="search" class="form-control" id="search"
                 placeholder="Search location">
          <label for="search">Search location</label>
        </div>
        <div v-if="locations" style="height: 30rem; margin-bottom: 2rem; overflow: auto">
          <div class="list-group">
            <a
                href="#"
                v-for="location in locations"
                :key="location.id"
                @click="selectLocation(location); getWeather(location)"
                class="list-group-item list-group-item-action"
            >
              {{ location.name }}
            </a>
          </div>
        </div>
      </div>
      <!-- Well, we've got a number of divs here  -->
      <div class="col-md-9">
        <div v-if="weather" :style="isWeatherLoading ? 'opacity: 0.2' : ''" class="row g-1">
          <div class="col-6 col-md-3 col-lg-2" v-for="data in weather" :key="data.time">
            <div class="card text-center">
              <div class="card-header">
                <small>{{ formatDate(data.time) }}</small>
              </div>
              <div class="card-body">
                <div>{{ data.temperature_2m_max }}<sup>{{ daily_units.temperature_2m_max }}</sup></div>
                <div>{{ data.temperature_2m_min }}<sup>{{ daily_units.temperature_2m_min }}</sup></div>
                <div class="border-top">
                  <small>
                    <sup
                        :style="data.precipitation_probability_max < 50 ? 'filter: grayscale(100%); opacity: 0.4' : ''">
                      🌧
                    </sup>
                    {{ data.precipitation_probability_max ? data.precipitation_probability_max : 0 }}
                    {{ daily_units.precipitation_probability_max }}
                  </small>
                </div>
                <div class="small border-top">
                  <div>☴</div>
                  {{ data.wind_speed_10m_max }} <sup>{{ daily_units.wind_speed_10m_max }}</sup>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import {debounce} from "debounce";

export default {
  name: "WeatherForecast",

  data() {
    return {
      location: { // A default location for first page load TODO: Get it dynamically
        name: 'Zanzibar',
        code: 'ZNZ',
        country_name: 'Tanzania',
        country_code: 'TZ',
        coordinates: {
          lat: -6.218466,
          lon: 39.221184
        }
      },
      locations: [],
      search: 'Tanzania',
      weather: null,
      isWeatherLoading: false,
    };
  },
  created: function () {
    this.locationAutocomplete();
    this.getWeather(this.location);
  },
  methods: {
    formatDate(dateString) {
      const inputDate = new Date(dateString);
      const options = {day: 'numeric', month: 'short'};
      return new Intl.DateTimeFormat('en-US', options).format(inputDate);
    },
    selectLocation(location) {
      this.location = location
    },
    locationAutocomplete: debounce( // For faster MVP we call the external API directly from here. TODO: Make Endpoint on Backend
        async function () {
          try {
            if (!this.search) {
              return
            }
            const response = await fetch(`https://autocomplete.travelpayouts.com/places2?locale=en&types[]=airport&types[]=city&term=${this.search}`);
            this.locations = await response.json();

          } catch (error) {
            console.error('Error fetching weather:', error);
          }
        },
        400 // A little delay to limit excessive API calls and provide smoother UX
    ),
    async getWeather(location) {
      this.isWeatherLoading = true;
      try {
        const response = await fetch(`http://127.0.0.1:8000/weather/?latitude=${location.coordinates.lat}&longitude=${location.coordinates.lon}`);
        const responseData = await response.json();

        this.weather = responseData.weather;
        this.daily_units = responseData.daily_units;

      } catch (error) {
        console.error('Error fetching weather:', error);
      }
      this.isWeatherLoading = false;
    },
  },
};
</script>
