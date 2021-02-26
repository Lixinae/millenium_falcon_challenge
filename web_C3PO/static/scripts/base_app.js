// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const base_app_vue = new Vue({
    el: '#app',
    data: {
        input_fields: {
            upload_file: "",
        },
        answer_data: {
            upload_file_json_answer: {},
            odds_of_success: -1,
            trajectory: {},
            refueled_on: {}
        }

    },
    methods: {
        submit_file() {
            let formData = new FormData();
            formData.append('file', this.input_fields.upload_file);
            let post_url = Flask.url_for("api_bp.upload_file_api")
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
                self.add_planets_to_display()

                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.error(JSON.stringify(response.message));
                console.log('FAILURE!!');
            });
        },
        handle_file_upload() {
            this.input_fields.upload_file = this.$refs.file.files[0];
        },
        // add_file(f) {
        //     let dropped_files = f.dataTransfer.files
        //     if (!dropped_files){
        //         return;
        //     }
        //     // On ne veut qu'un seul fichier
        //     if (dropped_files.length > 1){
        //         return;
        //     }
        //     this.input_fields.upload_file = dropped_files[0]
        //     // dropped_files.forEach(f =>{
        //     //     this.files.push(f);
        //     // });
        // },
        // remove_file(file){
        //     if (file === this.upload_file){
        //         this.input_fields.upload_file = ""
        //     }
        // },
        add_planets_to_display() {
            if (this.answer_data.trajectory.length > 0) {
                let trajectory_display_planets = $(".trajectory_display_planets")
                trajectory_display_planets.html("")
                let self = this
                $.each(this.answer_data.trajectory, function (key, planet_name) {
                    let file_name = "img/" + planet_name + "_128.png"
                    let url_img = Flask.url_for("static", {"filename": file_name})// Proviens du package JsGlue
                    let start_figure = "<figure>"
                    let planet_img = "<img class=\"planet_img\" src=\'" + url_img + "\' alt=\"Planet:" + planet_name + " miniature\">"
                    let figure_caption = "<figcaption class='fig_caption'>" + planet_name + "</figcaption>"
                    let end_figure = "</figure>"
                    let url_arrow = Flask.url_for("static", {"filename": "img/arrow_glow.png"})
                    let arrow_img = "<img class=\"arrow_img\" src=\'" + url_arrow + "\' alt=\"Planet:" + planet_name + " miniature\">"
                    let output = start_figure + planet_img + figure_caption + end_figure

                    if (key < self.answer_data.trajectory.length - 1) {
                        output += arrow_img;
                    }
                    trajectory_display_planets.append(output);
                });
            }
        }
    },
    delimiters: ["<%", "%>"], // delimiters specifique pour eviter les conflits avec jinja
    computed: {
        upload_disabled() {
            return this.input_fields.upload_file.length === 0;
        }
    }
});