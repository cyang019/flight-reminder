<template>
  <div class="card card-body">
    <ul class="list-group list-group-flush">
      <li v-if="dateIndicator===1" class="list-group-item july"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li v-else-if="dateIndicator===2" class="list-group-item august"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li v-else-if="dateIndicator===3" class="list-group-item september"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li v-else-if="dateIndicator===4" class="list-group-item october"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li v-else-if="dateIndicator===5" class="list-group-item november"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li v-else class="list-group-item othermonths"
        v-bind:class="monthColorObj"
      >
        {{formatDate(flightDate)}} {{flightNumber}}
      </li>
      <li class="text-primary list-group-item">
        {{currency}} {{price}}
      </li>
      <li class="list-group-item">
        {{fromAirport}} <span>-</span> {{toAirport}}
      </li>
      <li class="list-group-item">
        {{plane}}
      </li>
      <li class="list-group-item bg-light">
        <small>Last updated: {{foundTime}}</small>
      </li>
    </ul>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'flight-details',
  props: ['flight'],
  computed: {
    flightDate () {
      const flight_str = this.flight[0].split(':')[0]
      return moment(flight_str)
    },
    dateIndicator () {
      const flight_date = this.flightDate
      if (flight_date.isBefore(this.beginOfAugust)) {
        return 1
      } else if (flight_date.isBefore(this.beginOfSeptember)) {
        return 2
      } else if (flight_date.isBefore(this.beginOfOctober)) {
        return 3
      } else if (flight_date.isBefore(this.beginOfNovember)) {
        return 4
      } else {
        return 10
      }
    },
    flightNumber () {
      const number_str = this.flight[0].split(':')[1]
      return String(number_str)
    },
    currency () {
      const res = this.flight[1].split(' ')[0]
      return String(res)
    },
    price () {
      const res = this.flight[1].split(' ')[1]
      return String(res)
    },
    plane () {
      return String(this.flight[2])
    },
    fromAirport () {
      return String(this.flight[5])
    },
    toAirport () {
      return String(this.flight[6])
    },
    foundTime () {
      return String(this.flight[9])
    }
  },
  methods: {
    formatDate (value) {
      if (value) {
        return moment(String(value)).format('YYYY-MM-DD')
      }
    }
  },
  data () {
    return {
      beginOfAugust: moment('2020-08-01'),
      beginOfSeptember: moment('2020-09-01'),
      beginOfOctober: moment('2020-10-01'),
      beginOfNovember: moment('2020-11-01'),
      monthColorObj: {
        july: parseInt(this.dateIndicator) === 1,
        august: parseInt(this.dateIndicator) === 2,
        september: parseInt(this.dateIndicator) === 3,
        october: parseInt(this.dateIndicator) === 4,
        november: parseInt(this.dateIndicator) === 5,
        othermonth: parseInt(this.dateIndicator) === 10,
      }
    }
  }  
}
</script>

<style scoped>
  .july {
    background-color: #ED0026;
    color: #FFFFFF;
  }
  .august {
    background-color: #FA9D00;
    color: #FFFFFF;
  }
  .september {
    background-color: #FFD08D;
    color: #FFFFFF;
  }
  .october {
    background-color: #00909E;
    color: #FFFFFF;
  }
  .november {
    background-color: #006884;
    color: #FFFFFF;
  }
  .othermonths {
    background-color: #6E006C;
    color: #FFFFFF;
  }
</style>
