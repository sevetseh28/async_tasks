<template>
    <v-container grid-list-md>

        <v-layout row wrap>
            <v-flex xs12>
                <v-card>
                    <v-card-text>
                        <v-form v-model="valid" ref="form">

                            <v-container grid-list-md>
                                <v-layout>

                                    <v-flex xs6>
                                        <v-select
                                                v-model="problem_type"
                                                :items="problem_types"
                                                :rules="[rules.required]"
                                                label="Problem type"
                                                required
                                        ></v-select>
                                    </v-flex>

                                    <v-flex xs6>
                                        <v-text-field
                                                v-model="argument"
                                                :rules="[rules.isJson]"
                                                label="Argument"
                                                required
                                        ></v-text-field>
                                    </v-flex>


                                    <v-btn :loading="addLoading" @click="createTask()" :disabled="!valid" fab dark
                                           color="indigo">
                                        <v-icon dark>add</v-icon>
                                    </v-btn>
                                </v-layout>

                            </v-container>
                        </v-form>

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
                problem_type: null,
                argument: '',
                addLoading: false,
                valid: false,
                rules: {
                    isJson: function (value) {
                        try {
                            JSON.parse(value);
                            return true;
                        }
                        catch (err) {
                            return 'Must be a number for prime factoring or a list of numbers for integration'
                        }
                    },
                    required: v => !!v || 'Field is required'
                },
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
                if (this.$refs.form.validate()) {
                    var argval = this.argument;
                    var probval = this.problem_type;
                    this.addLoading = true;
                    axios.post('/api/problem/', {
                        'problem_type': probval,
                        'argument': JSON.parse(argval)
                    }).then(resp => {
                        this.tasks.unshift(resp.data);
                        this.addLoading = false;
                    }).catch(err => {
                        this.addLoading = false;
                        alert(err)  // should be handled prettier for the user
                    });
                    this.clear()
                }
            },

            clear() {
                this.$refs.form.reset()
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