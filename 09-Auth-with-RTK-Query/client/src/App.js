
import { Route, Switch } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'
import Authentication from './components/Authentication'
import { useAutoLoginQuery } from './app/services/userApi'

function App() {
  const [productions, setProductions] = useState([])
  // const [user, setUser] = useState(null)

  const {
    data: user=null,
    error,
    isLoading,
    isFetching,
    isUninitialized,
    isSuccess,
    isError,
  } = useAutoLoginQuery()
  console.log("🚀 ~ file: App.js:26 ~ App ~ isError:", isError)
  console.log("🚀 ~ file: App.js:26 ~ App ~ isSuccess:", isSuccess)
  console.log("🚀 ~ file: App.js:26 ~ App ~ isUninitialized:", isUninitialized)
  console.log("🚀 ~ file: App.js:26 ~ App ~ isFetching:", isFetching)
  console.log("🚀 ~ file: App.js:26 ~ App ~ isLoading:", isLoading)
  console.log("🚀 ~ file: App.js:26 ~ App ~ error:", error)
  console.log("🚀 ~ file: App.js:19 ~ App ~ user:", user)

  useEffect(() => {
    // fetchUser()
    fetchProductions()
  },[])

  const fetchProductions = () => (
    fetch('/productions')
    .then(res => res.json())
    .then(setProductions)
  )

  // const fetchUser = () => (
  //   fetch('/authorized')
  //   .then(res => {
  //     if(res.ok){
  //       res.json()
  //       .then(data => {
  //         setUser(data)
  //       })
  //     } else {
  //       setUser(null)
  //     }
  //   })
  // )
 
  const addProduction = (production) => setProductions(current => [...current,production])
  
  // const updateUser = (user) => setUser(user)
  if(!user) return (
    <>
      <GlobalStyle />
      <Navigation/>
      <Authentication />
    </>
  )

  return (
    <>
    <GlobalStyle />
    <Navigation />
      <Switch>
        <Route path='/productions/new'>
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail />
        </Route>
        <Route exact path='/authentication'>
          <Authentication />
        </Route>
        <Route exact path='/'>
          <Home  productions={productions}/>
        </Route>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `

