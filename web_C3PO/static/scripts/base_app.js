import Vue from 'vue'

// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const base_app_vue = new Vue({
    el: '#',
    data: {
        word: '',
        language_select: '',
        response_data: [],
        show_results: false,
        request_done: false
    },
    methods: {
        postData: function () {
            // console.log({word: this.word, language_select: this.language_select});
            // let post_url = $("#anagramos_post_form").attr("action"); //get form action url
            // let self = this; // Permet d'utiliser le this de la Vue
            // axios.post(post_url, {word: this.word, language_select: this.language_select})
            //     .then(function (response) {
            //         // Attention au this ici -> Le this ici est celui de Axios et pas de l'objet Vue
            //         self.response_data = response.data.results;
            //         self.show_results = true;
            //         self.request_done = true;
            //     })
            //     .catch(error => {
            //         console.log(error)
            //     });
        }
    },
    delimiters: ["<%", "%>"] // delimiters specifique pour eviter les conflits avec jinja
});