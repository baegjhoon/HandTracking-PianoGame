import React from 'react'

function Home() {
  return (
    <>
        <h1>가상 피아노 리듬 게임</h1>
        <input type="text" placeholder="닉네임을 입력해주세요 !" className="input input-bordered input-primary w-full max-w-xs" />
        <button className="btn btn-outline btn-primary">시작!</button>
    </>
  )
}

export default Home