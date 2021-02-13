
const clickSuggest = e => {

    const element = e.target
    document.getElementById(`${element.dataset.target}-input`).value = element.textContent;
    const type = document.getElementById("id_evaluation_type")
    type.options[element.dataset.type_id-1].selected = true;

};


document.addEventListener('DOMContentLoaded', e => {
    for (const element of document.getElementsByClassName('suggest')) {
        
        const targetName = element.dataset.target;
        const suggestListElement = document.getElementById(`${targetName}-list`);
        
        element.addEventListener('keyup', ()=> {
            const keyword = element.value;
            
            const url = `${element.dataset.url}?keyword=${keyword}`;
            console.log(url)
            
            if (keyword) {
                
                fetch(url)
                    .then(response => {
                        return response.json();
                    })
                    .then(response => {
                        const frag = document.createDocumentFragment();
                        suggestListElement.innerHTML = '';
                        
                        for (const obj of response.object_list) {
                        
                            const li = document.createElement('li');
                            li.textContent = obj.content;
                            li.dataset.pk = obj.pk;
                            li.dataset.target = targetName;
                            li.dataset.type_id = obj.type_id;
                            li.addEventListener('mousedown', clickSuggest);
                            frag.appendChild(li);
                        
                        }
                        
                        if (frag.children.length != 0) {
                        
                            suggestListElement.appendChild(frag);
                            suggestListElement.style.display = 'block';
                        } else {
                            suggestListElement.style.display = 'none';
                        }
                    
                    
                    })
                    .catch(error => {
                    
                        console.log(error);
                    });
            
            
            }
        
        });
        
        element.addEventListener('blur', () => {
        
            suggestListElement.style.display = 'none';
        });
        
        
    }

});