// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const base_app_vue = new Vue({
    el: '#app',
    data: {
        input_fields: {
            upload_file: "",
        },
        answer_data: {
            upload_file_json_answer: {},
            odds_of_success: 0,
            trajectory: {},
            refueled_on: {}
        }

    },
    methods: {
        submit_file() {
            let formData = new FormData();
            formData.append('file', this.upload_file);
            let post_url = $("#submit_file_and_comput_data_form").attr("action");
            let self = this;
            axios.post(post_url,
                formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(function (response) {
                self.answer_data.upload_file_json_answer = response.data.upload_file_json_answer;
                self.answer_data.odds_of_success = response.data.odds_of_success;
                self.answer_data.trajectory = response.data.trajectory;
                self.answer_data.refueled_on = response.data.refueled_on;
                console.log('SUCCESS!!');
            }).catch(function (response) {
                //console.log(response)
                console.log('FAILURE!!');
            });
        },
        handle_file_upload() {
            this.upload_file = this.$refs.file.files[0];
            // console.log('>>>> 1st element in files array >>>> ', this.upload_file);
        },
    },
    delimiters: ["<%", "%>"] // delimiters specifique pour eviter les conflits avec jinja
});