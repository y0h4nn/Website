var FormSet = function(empty_id, button_id, formset_id, nb_forms_id){
    this.empty = document.getElementById(empty_id);
    this.button = document.getElementById(button_id);
    this.formset = document.getElementById(formset_id);
    this.nb_forms = document.getElementById(nb_forms_id);
    this.button.addEventListener('click', function(event){
        event.preventDefault();
        var nb = this.formset.getElementsByTagName('tr').length
        var node = document.createElement('tr');
        node.innerHTML = this.empty.innerHTML.replace(new RegExp('__prefix__', 'g'), nb)
        this.nb_forms.value = nb + 1;
        this.formset.insertBefore(node, null);
    }.bind(this));
}
