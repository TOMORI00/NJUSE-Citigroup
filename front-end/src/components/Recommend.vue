<template>
  <div>
    <p>Recommend</p>
    <GChart type="LineChart" :data=chartData :options="chartOption"/>
  </div>
</template>

<script>
    import {GChart} from 'vue-google-charts';

    export default {
        name: "Recommend",
        data() {
            return {
                chartOption: {
                    charts: {
                        title: 'testChart'
                    },
                    focusTarget: 'category'
                }
            }
        },
        props: {
            chartData: [],
        },
        components: {
            GChart
        }
    }
</script>

<style scoped>

</style>