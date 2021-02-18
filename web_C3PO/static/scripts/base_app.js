// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const base_app_vue = new Vue({
    el: '#app',
    data: {
        upload_file: "",
        upload_file_json_answer:{},
        calculated_probability_of_caught:-1
    },
    methods: {
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.upload_file);
            let post_url = $("#upload_file_url").html();
            let self = this;
            axios.post(post_url,
                formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(function (response) {
                self.upload_file_json_answer = response.data
                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.log(response)
                console.log('FAILURE!!');
            });
        },
        handleFileUpload() {
            this.upload_file = this.$refs.file.files[0];
            console.log('>>>> 1st element in files array >>>> ', this.upload_file);
        }
    },
    delimiters: ["<%", "%>"] // delimiters specifique pour eviter les conflits avec jinja
});