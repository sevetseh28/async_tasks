<template>
    <v-container grid-list-md>

        <v-layout row wrap>
            <v-flex xs12>
                <v-card>
                    <v-card-text>
                        <v-container grid-list-md>
                            <v-layout>

                                <v-flex xs6>
                                    <v-select
                                            v-model="problem_type"
                                            :items="problem_types"
                                            label="Problem type"
                                    ></v-select>
                                </v-flex>

                                <v-flex xs6>
                                    <v-text-field
                                            v-model="argument"
                                            label="Argument"
                                            required
                                    ></v-text-field>
                                </v-flex>


                                <v-btn @click="createTask()" fab dark color="indigo">
                                    <v-icon dark>add</v-icon>
                                </v-btn>
                            </v-layout>

                        </v-container>
                    </v-card-text>


                </v-card>
            </v-flex>
            <v-flex xs12>


                <v-data-table
                        :headers="headers"
                        :items="tasks"
                        class="elevation-1">
                    <template slot="items" slot-scope="props">
                        <tr>
                            <td class="text-xs-left">{{ props.item.problem_type }}</td>
                            <td class="text-xs-left">{{ props.item.argument }}</td>

                            <v-chip :color="getStatusColor(props.item)"
                                    text-color="white">{{ props.item.state_realtime }}
                            </v-chip>
                            <td class="text-xs-left">{{ props.item.result_realtime }}</td>

                        </tr>
                    </template>
                </v-data-table>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "TasksList",
        data() {
            return {
                problem_types: ['Integrate', 'Prime factoring'],
                problem_type: '',
                argument: '',
                tasks: [],
                headers: [
                    {
                        text: 'Problem type',
                        align: 'left',
                        sortable: false,
                        value: 'problem_type'
                    },
                    {text: 'Arguments', value: 'argument'},
                    {text: 'Status', value: 'status'},
                    {text: 'Result', value: 'result'},
                ],
            }
        },
        methods: {
            getDataFromApi() {
                axios.get('/api/problem/').then(resp => {
                    this.tasks = resp.data;
                });
            },

            createTask() {
                axios.post('/api/problem/', {'problem_type': this.problem_type, 'argument': JSON.parse(this.argument)}).then(resp => {
                });
            },

            getStatusColor(item) {
                var status = item.state_realtime;
                if (status === 'SUCCESS') {
                    return 'green'
                } else if (status === 'FAILURE') {
                    return 'red'
                } else if (status === 'PENDING') {
                    return 'blue'
                } else {
                    return 'grey'
                }
            }


        },
        mounted() {

            this.getDataFromApi();
            setInterval(function () {
                this.getDataFromApi();
            }.bind(this), 8000);
        },
    }
</script>

<style scoped>

</style>