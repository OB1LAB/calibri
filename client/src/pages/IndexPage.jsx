import React, { useEffect } from "react";
import "../styles/Index.css";

export default function IndexPage() {
  useEffect(() => {
    document.title = "Информация";
  }, []);

  return (
    <div>
      <h1>
        В честь завершение написания сайта, всем даётся бонус в виде 1500
        баллов!
      </h1>
      <h1>
        Для получения вам нужно войти в систему и нажмить{" "}
        <a
          className="trololo"
          href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        >
          сюда
        </a>
      </h1>
    </div>
  );
}
