import React from "react";
import Select from "react-select";

const style = {
  control: (base) => ({
    ...base,
    border: 1,
    outline: "1px solid black",
  }),
};

export default function Selector({
  options,
  defaultValue,
  onChange,
  isMulti,
  closeMenuOnSelect,
  value,
  placeholder,
}) {
  return (
    <div style={{ width: "100%" }}>
      <Select
        hideSelectedOptions={true}
        value={value}
        styles={style}
        options={options}
        isSearchable={false}
        defaultValue={defaultValue}
        onChange={onChange}
        isMulti={isMulti}
        closeMenuOnSelect={closeMenuOnSelect}
        placeholder={placeholder}
        noOptionsMessage={() => {
          return "Все элементы выбраны";
        }}
        theme={(theme) => ({
          ...theme,
          borderRadius: 0,
          colors: {
            ...theme.colors,
            primary25: "#DFDFDF",
            primary: "#1e1e1e",
            primary50: "#DFDFDF",
            neutral0: "#F0F0F0",
            neutral20: "black",
            neutral30: "black",
            neutral10: "#D6D6D6",
            danger: "black",
            dangerLight: "#C1C1C1",
          },
        })}
      />
    </div>
  );
}
