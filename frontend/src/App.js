import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ]
    }
  }

  addNewContact = (event) => {

    let updatedContacts = this.state.contacts;

    updatedContacts.push({
      id: updatedContacts.length+1,
      name: event.target.name.value,
      nickname: event.target.nickname.value,
      hobby: event.target.nickname.value,
    });

    this.setState({
      contacts: updatedContacts,
    });

    this.refs.count.incrementCount();

    event.preventDefault();
  }

  resetForm = () => { 
    document.getElementById("addContactForm").reset();
  }

  render() {
    return (
      <div className="App">
        <Instructions complete = {true}/>

        {this.state.contacts.map(x => (
          <Contact id={x.id} name={x.name} nickcname={x.nickname} hobby={x.hobby} />
        ))}

        <Counter ref="count"/>
        <br/>

        <p>Add a New Contact Below:</p>

        <form id = "addContactForm" onSubmit={this.addNewContact}>
          <input name="name" type="text" placeholder="Contact's name" /> 
          <input name="nickname" type="text" placeholder="Contact's nickname" />
          <input name="hobby" type="text" placeholder="Contact's hobby" /> <br/>
          <input type="submit" value="Add New Contact!" />
          <input name="clearForm" type="button" value="Clear Form" onClick={this.resetForm}/>
        </form>
      </div>
    )
  }
}

export default App
