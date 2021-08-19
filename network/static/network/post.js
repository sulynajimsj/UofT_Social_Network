
function follow(id){
    let followBtn = document.querySelector('#follow');
    let following = document.querySelector('#following');
    let followers = document.querySelector('#followers');

    

    if (followBtn.innerHTML == "Follow"){
        fetch('/follow/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                follow: true
            })
          }).then(()=>{
            fetch('/follow/' + id)
            .then(response=>response.json())
            .then(data => {
                following.innerHTML = data[0]
                followers.innerHTML = data[1]
            })

                followBtn.innerHTML = "Unfollow";
          })
        

    }
    else if (followBtn.innerHTML == "Unfollow"){
        fetch('/follow/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                follow: false
            })
          }).then(()=>{
            fetch('/follow/' + id)
            .then(response=>response.json())
            .then(data => {
                following.innerHTML = data[0]
                followers.innerHTML = data[1]
            })

                followBtn.innerHTML = "Follow";
          })
          

    }
}



function like(id){
    let like = document.querySelector(`#heart${id}`);
    let counter = document.querySelector(`#counter${id}`);
    let liked = true;

    fetch('/like/' + id)
        .then(response=>response.json())
        .then(data => {
            liked = data[1]
        }).then(function(){
            if (liked){
                
                fetch('/like/' + id, {
                    method: 'PUT',
                    body: JSON.stringify({
                        likes: false
                    })
                  }).then(function(){
                    fetch('/like/' + id)
                    .then(response=>response.json())
                    .then(data => {
                        counter.innerHTML = data[0];
                    })
        
                  })
             
                like.style.color = 'black';
            }
            else{
                
                fetch('/like/' + id, {
                    method: 'PUT',
                    body: JSON.stringify({
                        likes: true
                    })
                  }).then(function(){
                    fetch('/like/' + id)
                    .then(response=>response.json())
                    .then(data => {
                        counter.innerHTML = data[0];
                        
            
                    })
        
                  })
        
                like.style.color = 'red';
                
        
            }
        })
  
    
}
function edit(id){
    let editBtn = document.querySelector(`#edit${id}`);
    let saveBtn = document.querySelector(`#save${id}`);
    let editBox = document.querySelector(`#edit-text${id}`);
    let postDes = document.querySelector(`#postDes${id}`);

    saveBtn.style.display = 'block';
    editBox.style.display = 'block';
    editBtn.style.display = 'none';
    

    saveBtn.onclick = function(){
        fetch('/edit/'+id, {
            method: 'PUT',
            body: JSON.stringify({
                des: editBox.value
            })
          });

          postDes.innerHTML = editBox.value;


        
          saveBtn.style.display = 'none';
          editBox.style.display = 'none';
          editBtn.style.display = 'block';

    }    
    
}

        

    
 







