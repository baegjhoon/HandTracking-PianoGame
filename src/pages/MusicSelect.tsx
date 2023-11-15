import React from "react";

import MusicSelectNavbar from "../components/MusicSelectNavbar";
import MusicLists from "../containers/MusicLists";

function MusicSelect() {
  return (
    <>
        <MusicSelectNavbar />
        <MusicLists />
    </>
  );
}

export default MusicSelect;
