import React from "react";
import Selector from "./Selector";

const categories = {
  tmrpg: [
    { value: "Thaumcraft", label: "Thaumcraft" },
    { value: "Vanila", label: "Vanila" },
    { value: "IC2", label: "IC2" },
    { value: "Avaritia", label: "Avaritia" },
    { value: "AE2", label: "AE2" },
    { value: "Advanced Solar Panels", label: "Advanced Solar Panels" },
    { value: "Draconic Evolution", label: "Draconic Evolution" },
    { value: "Divine RPG", label: "Divine RPG" },
    { value: "Ender IO", label: "Ender IO" },
    { value: "Extra Utilities", label: "Extra Utilities" },
  ],
  dt: [
    { value: "Draconic Evolution", label: "Draconic Evolution" },
    { value: "IC2", label: "IC2" },
    { value: "Vanila", label: "Vanila" },
    { value: "AE2", label: "AE2" },
    { value: "Advanced Solar Panels", label: "Advanced Solar Panels" },
    { value: "Extra Utilities", label: "Extra Utilities" },
    { value: "Avaritia", label: "Avaritia" },
    { value: "Ender IO", label: "Ender IO" },
    { value: "Other", label: "Другое" },
  ],
};

export default function SelectCategories({
  categoriesFilter,
  selectedServer,
  onChange,
}) {
  return (
    <Selector
      value={categoriesFilter}
      options={categories[selectedServer]}
      isMulti={true}
      closeMenuOnSelect={false}
      onChange={onChange}
      placeholder="Категории..."
    />
  );
}
