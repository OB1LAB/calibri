import React from "react";
import Selector from "./Selector";

const servers = [
  { value: "dt", label: "DraconicTech" },
  { value: "tmrpg", label: "TechnoMagicRPG" },
];

export default function SelectServer({ onChange, value }) {
  if (value) {
    return <Selector options={servers} value={value} onChange={onChange} />;
  }
  return (
    <Selector options={servers} defaultValue={servers[0]} onChange={onChange} />
  );
}
