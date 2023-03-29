// Display
// document.getElementById('display').innerHTML = `<li class="list-group-item">id : ${data.id} Name : ${data.name} Genre : ${data.email} Game : ${data.password}</li>`
// document.getElementById('display').innerHTML = `<li class="list-group-item"> Content </li>`

fetch(`http://127.0.0.1:5000`)
.then(res => res.json())
.then((data) => {
    // document.getElementById('display').innerHTML = `<li class="list-group-item">id : ${data.id} Name : ${data.name} Email : ${data.email} Password : ${data.password}</li>`

    let dis= "";
    for (var i = 0; i < data.length; i++) {
        // console.log(data[i].name + " is " + data[i].age + " years old.");
        dis += `<li class="list-group-item">id : ${data[i].id} Name : ${data[i].name} Email : ${data[i].email} Password : ${data[i].password}</li>`
    }
    document.getElementById('display').innerHTML = dis
})

// GET
document.getElementById('formData').addEventListener('submit', retrieveName);
function retrieveName(e) {
    e.preventDefault();
    let id = document.getElementById('id').value

    fetch(`http://127.0.0.1:5000/${id}`)
    .then(res => res.json())
    .then((data) => {
        console.log(data)
        document.getElementById('result').innerHTML = `<li class="list-group-item">id : ${data.id} Name : ${data.name} Email : ${data.email} Password : ${data.password}</li>`
    })
}


// POST
document.getElementById('postData').addEventListener('submit', postData)

function postData (e) {
    e.preventDefault()

    let id = document.getElementById('postId').value
    let name = document.getElementById('postName').value
    let mail = document.getElementById('postEmail').value
    let password = document.getElementById('postPassword').value

    console.log(id, name, mail, password)

    fetch('http://127.0.0.1:5000/postData', {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({
            'id' : id,
            'name' : name,
            'email' : mail,
            'password' : password
        })
    })
    .then((response) => response.json())
    .then((data) => console.log(data))
}


// // UPDATE
// document.getElementById('updateData').addEventListener('submit', postData)

// function postData (e) {
//     e.preventDefault()
//     let currid = document.getElementById('CurrUpdatedtId').value
//     let id = document.getElementById('updatedtId').value
//     let name = document.getElementById('updatedtName').value
//     let mail = document.getElementById('updatedtEmail').value
//     let password = document.getElementById('updatedtPassword').value
//     let repassword = document.getElementById('updatedtRePassword').value
//     console.log(id, name, mail, password)

//     fetch('http://127.0.0.1:5000/update/<currid>', {
//         method : 'POST',
//         headers : {
//             'Content-Type' : 'application/json'
//         },
//         body : JSON.stringify({
//             'id' : id,
//             'name' : name,
//             'email' : mail,
//             'password' : password,
//             'passwordCheck' : repassword
//         })
//     })
//     .then((response) => response.json())
//     .then((data) => console.log(data))
// }




// // DELETE
// document.getElementById('delData').addEventListener('submit', delName);
// function delName(e) {
//     e.preventDefault();
//     let id = document.getElementById('delId').value

//     console.log(id)
//     fetch(`http://127.0.0.1:5000/deleteData/${id}`)
//     .then(res => res.json())
//     .then((data) => {
//         console.log(data)
//         // document.getElementById('result').innerHTML = `<li class="list-group-item">id : ${data.id} Name : ${data.name} Email : ${data.email} Password : ${data.password}</li>`
//     })
// }