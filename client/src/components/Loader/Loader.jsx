import { Blocks } from "react-loader-spinner";
import classes from "./Loader.module.css";

export default function Loader() {
  return (
    <div className={classes.loader}>
      <Blocks
        visible={true}
        height="100"
        width="100"
        ariaLabel="blocks-loading"
        wrapperStyle={{}}
        wrapperClass="blocks-wrapper"
      />
    </div>
  );
}
