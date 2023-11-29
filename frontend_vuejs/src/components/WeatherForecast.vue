<template>

  <div id="weather-forecast" class="container">
    <div class="row row-cols-md-2">
      <div class="col fs-2">Weather Forecast</div>
      <div class="col fs-2">{{ location.name }}</div>
    </div>
    <div class="row mt-4">
      <div class="col col-md-3">
        <div class="form-floating mb-2">
          <input v-model="search" @input="locationAutocomplete" type="search" class="form-control" id="search"
                 placeholder="Search location">
          <label for="search">Search location</label>
        </div>
        <div v-if="locations" style="height: 20rem; margin-bottom: 2rem; overflow: auto">
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
      <div class="col-md-9">
        <div v-if="weather">
          <div class="row g-1">
            <div class="col-4 col-md-3 col-lg-2" v-for="data in weather.slice(0, 12)" :key="data.time">
              <div class="card text-center">
                <div class="card-header">
                  <small>{{ formatDate(data.time) }}</small>
                </div>
                <div class="card-body">
                  <div>{{ data.temperature_2m_max }}<sup>{{ daily_units.temperature_2m_max }}</sup></div>
                  <div>{{ data.temperature_2m_min }}<sup>{{ daily_units.temperature_2m_min }}</sup></div>
                  <div class="border-bottom">
                    <small>
                      <sup :style="data.precipitation_probability_max < 50 ? 'filter: grayscale(100%); opacity: 0.4' : ''">🌧</sup>
                      {{ data.precipitation_probability_max ? data.precipitation_probability_max : 0 }}
                      {{ daily_units.precipitation_probability_max }}
                    </small>
                  </div>
                  <div class="small">
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
  </div>

</template>

<script>
import {debounce} from "debounce";

export default {
  name: "WeatherForecast",

  data() {
    return {
      location: { // A default location for first page load
        name: 'Zanzibar',
        coordinates: {
          lat: -6.218466,
          lon: 39.221184
        }
      },
      locations: [],
      search: 'Tanzania',
      weather: null,
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

    locationAutocomplete: debounce(
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
        500
    ),
    async getWeather(location) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/weather/?latitude=${location.coordinates.lat}&longitude=${location.coordinates.lon}`);
        const responseData = await response.json();

        this.weather = responseData.weather;
        this.daily_units = responseData.daily_units;

      } catch (error) {
        console.error('Error fetching weather:', error);
      }
    },
  },
};
</script>
