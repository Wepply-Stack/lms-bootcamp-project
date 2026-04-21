import React from 'react'
import { Outlet } from 'react-router-dom'

const MainLayout = () => {
  return (
    <div className='main-layout min-h-screen w-full flex flex-col'>
      <main>
        <Outlet />
      </main>
       
    </div>
  )
}

export default MainLayout