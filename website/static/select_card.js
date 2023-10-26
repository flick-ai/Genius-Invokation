let available_character = null
let available_card = null
function modify_object(a){
available_character = a
}

function load_action_cards(a){
available_card = a
}
let select_character_result = []
let select_card_result = []

let startgame = document.getElementById('startgame')
startgame.addEventListener(
"click", ()=>{
    document.getElementById('gamestatus').innerText = 'start'
}
)

// 保存和读取卡组
let savecard = document.getElementById('saveselect')
let loadcard = document.getElementById('loadselect')
loadcard.innerText = '读取卡组' + `(角色${select_character_result.length})`
savecard.addEventListener(
"click", ()=>{
    saved_card = localStorage.getItem('saved_card')
    if (select_card_result.length != 0){
    name = prompt('请输入卡组名称')
    if (name == null){
        return
    } else {
        if (saved_card == null){
        saved_card = {}
        } else {
        saved_card = JSON.parse(saved_card)
        }
        saved_card[name] = {"character": select_character_result[select_character_result.length-1], "card": select_card_result[select_character_result.length-1]}
        localStorage.setItem('saved_card', JSON.stringify(saved_card))
        alert('保存成功')
    }
    }
}
)


loadcard.addEventListener(
"click", ()=>{
    saved_card = localStorage.getItem('saved_card')
    if (saved_card == null){
    alert('没有保存的卡组')
    } else {
    saved_card = JSON.parse(saved_card)
    saved_card_name = Object.keys(saved_card)
    saved_card_name_str = saved_card_name.join('\n')
    while(true){
        select_name = prompt('请输入卡组名称\n' + saved_card_name_str)
        if (select_name == null){
        return
        } else if (saved_card_name.includes(select_name)){
        break
        } else {
        alert('没有这个卡组')
        }
    }
    
    saved_card_item = saved_card[select_name]
    saved_character = saved_card_item["character"]
    document.getElementById('currentselect').innerText = saved_character
    has_selected = document.getElementById('hasselected')
    has_selected.innerText = has_selected.innerText + ' ' + saved_character
    select_character_result.push(saved_character)
    saved_card = saved_card_item["card"]
    document.getElementById('current_select_card').innerText = saved_card
    select_card_result.push(saved_card)
    if(select_character_result.length == 1){
        loadcard.style.display = 'flex'
        loadcard.innerText = '读取卡组' + `(角色${select_character_result.length})`
    } else if (select_character_result.length == 2){
        character_confirm.style.display = 'none'
        startgame.style.display = 'flex'
    }
    }
    
}
)


let cardtype = ["WEAPON_TALENT", "ARTIFACT", "SUPPORT", "SPECIAL_EVENT", "EVENT"]
let cardtypename = ["武器和天赋", "圣遗物",  "支援", "特殊事件", "事件"]
for(let i = 0; i<5; i++){
let cardtypebox = document.createElement('div')
cardtypebox.classList.add('selectcardinner')
cardtypebox.classList.add('item')
let cardtypeboxtitle = document.createElement('div')
cardtypeboxtitle.classList.add('item')
cardtypeboxtitle.innerText = cardtypename[i]
let cardtypeboxcontent = document.createElement('div')
cardtypeboxcontent.classList.add('item')
cardtypeboxcontent.classList.add('selectcardinnercontent')
cardtypeboxcontent.id = cardtype[i]
cardtypebox.appendChild(cardtypeboxtitle)
cardtypebox.appendChild(cardtypeboxcontent)
document.getElementById("selectcard").appendChild(cardtypebox)
}

async function get_card() {
while(true){
    if(available_card){
    let resdict = available_card.toJs()
    available_card = resdict
    console.log(resdict)
    let cur_idx = 0
    for(var [name, cardlist] of resdict){
        let cardtypeboxcontent = document.getElementById(cardtype[cur_idx])
        for(let i = 0; i<cardlist.length; i++){
        let card = cardlist[i]
        let checkdiv = document.createElement('div')
        checkdiv.classList.add('checkdiv', 'item', 'clickable', 'carditem')
        checkdiv.innerText = card[2]
        let nothing = document.createElement('div')
        nothing.classList.add('nothing')
        nothing.innerText = card[0]
        checkdiv.appendChild(nothing)
        checkdiv.addEventListener(
            "click", ()=>{
            if(checkdiv.classList.contains('twice')){
            checkdiv.classList.remove('twice')
            checkdiv.classList.remove('selected')
            value = checkdiv.getElementsByClassName('nothing')[0].innerText
            current_card_choice = current_card_choice.filter(element => {
                return element != value
            });
            
            }else if(checkdiv.classList.contains('selected')){
            checkdiv.classList.add('twice')
            value = checkdiv.getElementsByClassName('nothing')[0].innerText
            current_card_choice.push(value)
            }else{
            checkdiv.classList.add('selected')
            value = checkdiv.getElementsByClassName('nothing')[0].innerText
            current_card_choice.push(value)
            }
            card_confirm.innerText = '确定手牌(' + current_card_choice.length + '/30)'
            
            }
        )
        cardtypeboxcontent.appendChild(checkdiv)
        }
        cur_idx += 1
    }
    available_card = null
    break
    }
    await sleep(200)
}
}
let current_character_choice = new Set()
let current_card_choice = new Array()
let character_confirm = document.getElementById('confirmchara')
let card_confirm = document.getElementById('confirmcard')
card_confirm.style.display = 'none'
character_confirm.addEventListener(
"click", ()=>{
    if (current_character_choice.size != 3){
    alert('请选择3个角色')
    return
    }
    let data_string = ""
    for (const item of current_character_choice) {
    console.log(item)
    data_string += item + " "
    }
    data_string = data_string.trim()
    document.getElementById('currentselect').innerText = data_string
    select_character_result.push(data_string)
    current_character_choice.clear()
    for (const item of document.getElementsByClassName('charaitem')) {
    item.classList.remove('selected')
    }
    character_confirm.style.display = 'none'
    card_confirm.style.display = 'flex'
    loadcard.style.display = 'none'
    savecard.style.display = 'none'
    has_selected = document.getElementById('hasselected')
    has_selected.innerText = has_selected.innerText + ' ' + data_string
    get_card()
})


card_confirm.addEventListener(
"click", ()=>{
    if (current_card_choice.length != 30){
    alert('请选择30张手牌')
    return
    }
    let data_string = ""
    for (const item of current_card_choice) {
    console.log(item)
    data_string += item + " "
    }
    data_string = data_string.trim()
    document.getElementById('current_select_card').innerText = data_string
    select_card_result.push(data_string)
    current_card_choice = new Array()
    for(const item of document.getElementsByClassName('carditem')){
    item.classList.remove('selected')
    item.classList.remove('twice')
    item.style.display = 'none'
    }
    card_confirm.style.display = 'none'
    character_confirm.style.display = 'flex'
    savecard.style.display = 'flex'
    savecard.innerText = '保存卡组' + `(角色${select_character_result.length-1})`
    if (select_character_result.length == 1){
    loadcard.style.display = 'flex'
    loadcard.innerText = '读取卡组' + `(角色${select_character_result.length})`
    }
    else if (select_character_result.length == 2){
    character_confirm.style.display = 'none'
    startgame.style.display = 'flex'
    }
    
    

}
)

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
async function get_character() {
while(true){
    await sleep(200)
    if(available_character){
    let resdict = available_character.toJs()
    available_character = resdict
    console.log(resdict)
    for(var [key, value] of resdict) {
        let checkdiv = document.createElement('div')
        checkdiv.classList.add('checkdiv')
        checkdiv.classList.add('item', 'clickable', 'charaitem')
        checkdiv.innerText = key
        let nothing = document.createElement('div')
        nothing.classList.add('nothing')
        nothing.innerText = value
        checkdiv.appendChild(nothing)
        checkdiv.addEventListener(
        "click", ()=>{
            checkdiv.classList.toggle('selected')
            if(checkdiv.classList.contains('selected')){
            value = checkdiv.getElementsByClassName('nothing')[0].innerText
            current_character_choice.add(value)
            console.log(current_character_choice)
            }else{
            value = checkdiv.getElementsByClassName('nothing')[0].innerText
            current_character_choice.delete(value)
            }
        }
        )
        document.getElementById('selectcharacter').appendChild(checkdiv)

    }
    break
    }
}
}
get_character()