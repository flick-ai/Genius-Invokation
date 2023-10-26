let current_choice = ""
let current_choice_set = new Set()
let current_dice = ""
let current_dice_set = new Set()
function update_set(set, data){
  if (set.has(data)){
    set.delete(data)
  } else {
    set.add(data)
  }
  let data_string = ""
  for (const item of set) {
    data_string += item + " "
  }
  return data_string.trim()
}
let current_choice_text = document.getElementById("current_choice")
let current_dice_text = document.getElementById("current_dice")
let current_target = ""

// 切换角色和结束回合
let change_character = document.getElementsByClassName("changecharacter")[0]
change_character.addEventListener(
  "click", ()=>{
    change_character.classList.toggle("selected")
    current_choice = update_set(current_choice_set, "14")
    current_choice_text.innerText = current_choice

    // 不需要确认
    document.getElementById("input_result").innerText = current_choice + 't'
    current_choice_text.innerText = ""
    current_choice_set.clear()
    current_choice = ""
    clicker = document.getElementsByClassName("clickable")
    for (let i = 0; i < clicker.length; i++) {
      clicker[i].classList.remove("selected")
    }
  }
)
let passround = document.getElementsByClassName("passround")[0]
passround.addEventListener(
  "click", ()=>{
    passround.classList.toggle("selected")
    current_choice = update_set(current_choice_set, "15")
    current_choice_text.innerText = current_choice

    // 不需要确认
    document.getElementById("input_result").innerText = current_choice + 't'
    current_choice_text.innerText = ""
    current_choice_set.clear()
    current_choice = ""
    clicker = document.getElementsByClassName("clickable")
    for (let i = 0; i < clicker.length; i++) {
      clicker[i].classList.remove("selected")
    }
  }
)

// 手牌区

for (let index = 0; index < 2; index++) {
  let handcard_player = document.getElementsByClassName(`handcard player${index}`)[0]
  let handcard_inner = document.createElement('div');
  handcard_inner.className = 'handcardinner';
  handcard_player.appendChild(handcard_inner);
  for (let i = 0; i < 10; i++) {
    let card = document.createElement("div")
    card.classList.add("handcard")
    card.classList.add("clickable")
    card.id = `player${index}_card` + i
    card.innerText = ""
    card.addEventListener(
      "click", ()=>{
        card.classList.toggle("selected")
        // current_choice = `${i}`
        current_choice = update_set(current_choice_set, `${i}`)
        current_choice_text.innerText = current_choice
      }
    )
    handcard_inner.appendChild(card)
  }

  // 骰子区
  let dice_player = document.getElementsByClassName(`dice player${index}`)[0]
  let dice_inner = document.createElement('div');
  dice_inner.className = 'diceinner';
  dice_player.appendChild(dice_inner);
  let dice_name = dice_player.getElementsByClassName("thetitle")[0]
  dice_name.addEventListener(
    "click", ()=>{
      dice_name.classList.toggle("selected")
      current_choice = update_set(current_choice_set, "13")
      current_choice_text.innerText = current_choice
    }
  )
  for (let i = 0; i < 16; i++) {
    let newDiv = document.createElement('div');
    newDiv.className = 'gridItem';
    newDiv.classList.add("diceitem", "clickable")
    newDiv.addEventListener(
        "click", ()=>{
          newDiv.classList.toggle("selected")
          current_choice = update_set(current_choice_set, `${i}`)
          current_choice_text.innerText = current_choice
        }
      )
    newDiv.id = `player${index}_dice` + i
    newDiv.textContent = "";
    dice_inner.appendChild(newDiv);
  }

  let confirm_btn = document.createElement("div")
  confirm_btn.classList.add("item", "clickable")
  confirm_btn.addEventListener(
      "click", ()=>{
      document.getElementById("input_result").innerText = current_choice + 't'
      current_choice_text.innerText = ""
      current_choice_set.clear()
      current_choice = ""
      clicker = document.getElementsByClassName("clickable")
      for (let i = 0; i < clicker.length; i++) {
        clicker[i].classList.remove("selected")
      }
    }
  )
  confirm_btn.innerText = "确认"
  dice_player.appendChild(confirm_btn)

  // 支援区
  for (let support_idx = 0; support_idx < 4; support_idx++) {
    support_zone = document.getElementsByClassName(`support${support_idx} player${index}`)[0]
    let support_name = support_zone.getElementsByClassName("thetitle")[0]
    support_name.addEventListener(
      "click", ()=>{
        support_name.classList.toggle("selected")
        current_choice = update_set(current_choice_set, `${support_idx + 9}`)
        current_choice_text.innerText = current_choice
      }
    )
    support_inner = document.createElement('div');
    support_inner.classList.add("inneritem")
    // support_inner.className = 'supportinner';
    support_zone.appendChild(support_inner);

  }

  // 召唤区
  for (let summon_idx = 0; summon_idx < 4; summon_idx++) {
    summon_zone = document.getElementsByClassName(`summon${summon_idx} player${index}`)[0]
    let summon_name = summon_zone.getElementsByClassName("thetitle")[0]
    summon_name.addEventListener(
      "click", ()=>{
        summon_name.classList.toggle("selected")
        current_choice = update_set(current_choice_set, `${summon_idx + 5}`)
        current_choice_text.innerText = current_choice
      }
    )
    let summon_inner = document.createElement('div');
    summon_inner.classList.add("inneritem")
    // summon_name = document.createElement('div');
    summon_zone.appendChild(summon_inner);
  }

  // 角色区
  for (let chara_idx = 0; chara_idx < 3; chara_idx++) {
    chara_zone = document.getElementsByClassName(`character${chara_idx} player${index}`)[0]
    let chara_name = chara_zone.getElementsByClassName("thetitle")[0]
    chara_name.addEventListener(
      "click", ()=>{
        chara_name.classList.toggle("selected")
        current_choice = update_set(current_choice_set, `${chara_idx + 2}`)
        current_choice_text.innerText = current_choice
      }
    )
    let basebar = document.createElement("div")
    basebar.classList.add("basebar")
    let health_circle = document.createElement("div")
    health_circle.classList.add("health", "circle")
    health_circle.id = `player${index}_character${chara_idx}_health`
    let energy_circle = document.createElement("div")
    energy_circle.classList.add("energy", "circle")
    energy_circle.id = `player${index}_character${chara_idx}_power`
    let elemnt_circle = document.createElement("div")
    elemnt_circle.classList.add("element", "circle")
    elemnt_circle.id = `player${index}_character${chara_idx}_element`

    basebar.appendChild(health_circle)
    basebar.appendChild(energy_circle)
    basebar.appendChild(elemnt_circle)
    chara_zone.appendChild(basebar)

    let equipbar = document.createElement("div")
    equipbar.classList.add("basebar")
    let weapon_circle = document.createElement("div")
    weapon_circle.classList.add("equip", "circle")
    weapon_circle.id = `player${index}_character${chara_idx}_weapon`
    weapon_circle.innerText = "W"

    let waapon_circle_inner = document.createElement("div")
    waapon_circle_inner.classList.add("equipexpandinner")
    waapon_circle_inner.id = `player${index}_character${chara_idx}_weapon_inner`
    waapon_circle_inner.innerText = "武器"
    weapon_circle.appendChild(waapon_circle_inner)


    let artifact_circle = document.createElement("div")
    artifact_circle.classList.add("equip", "circle")
    artifact_circle.id = `player${index}_character${chara_idx}_artifact`
    artifact_circle.innerText = "A"

    let artifact_circle_inner = document.createElement("div")
    artifact_circle_inner.classList.add("equipexpandinner")
    artifact_circle_inner.id = `player${index}_character${chara_idx}_artifact_inner`
    artifact_circle_inner.innerText = "圣遗物"
    artifact_circle.appendChild(artifact_circle_inner)


    let talent_circle = document.createElement("div")
    talent_circle.classList.add("equip", "circle")
    talent_circle.id = `player${index}_character${chara_idx}_talent`
    talent_circle.innerText = "T"

    let talent_circle_inner = document.createElement("div")
    talent_circle_inner.classList.add("equipexpandinner")
    talent_circle_inner.id = `player${index}_character${chara_idx}_talent_inner`
    talent_circle_inner.innerText = "天赋"
    talent_circle.appendChild(talent_circle_inner)


    equipbar.appendChild(weapon_circle)
    equipbar.appendChild(artifact_circle)
    equipbar.appendChild(talent_circle)
    chara_zone.appendChild(equipbar)

    let skill_list = document.createElement("div")
    skill_list.classList.add("contain")
    for (let i = 0; i < 4; i++) {
      let skill = document.createElement("div")
      skill.id = `player${index}_character${chara_idx}_skill` + i
      skill.classList.add("skill", "clickable")
      skill.innerText = ""
      skill.addEventListener(
        "click", ()=>{
          skill.classList.toggle("selected")
          current_choice = update_set(current_choice_set, `${i+10}`)
          current_choice_text.innerText = current_choice
        }
      )
      skill_list.appendChild(skill)
    }
    chara_zone.appendChild(skill_list)
    let chara_state_box = document.createElement("div")
    let chara_state = document.createElement("div")
    chara_state.classList.add("expanditem")
    chara_state.innerText = "角色状态"

    chara_state.id = `player${index}_character${chara_idx}_state`
    


    let chara_state_inner = document.createElement("div")
    chara_state_inner.classList.add("expandinner")

    chara_state_inner.id = `player${index}_character${chara_idx}_state_inner`

    chara_state_inner.innerText = "角色状态"
    chara_state.appendChild(chara_state_inner)

    chara_state_box.appendChild(chara_state)

    chara_zone.appendChild(chara_state_box)

    let group_shield_box = document.createElement("div")
    let group_state = document.createElement("div")
    group_state.classList.add("expanditem")
    group_state.id = `player${index}_character${chara_idx}_group_state`
    group_state.innerText = "出战状态"
    
    let group_state_inner = document.createElement("div")
    group_state_inner.classList.add("expandinner")
    group_state_inner.id = `player${index}_character${chara_idx}_group_state_inner`
    group_state_inner.innerText = "出战状态"
    group_state.appendChild(group_state_inner)
    group_shield_box.appendChild(group_state)
    chara_zone.appendChild(group_shield_box)
    

  }

}

let confirm_action = document.getElementById("confirm_action")
confirm_action.addEventListener(
  "click", ()=>{
    document.getElementById("input_result").innerText = current_choice + 't'
    current_choice_text.innerText = ""
    current_choice_set.clear()
    current_choice = ""
    clicker = document.getElementsByClassName("clickable")
    for (let i = 0; i < clicker.length; i++) {
      clicker[i].classList.remove("selected")
    }
  }
)