import ReactMarquee from "react-easy-marquee";

export const Marquee = () => (
  <div
    className="
        bg-yellow uppercase dark:bg-dark-purple dark:text-white font-heading
        text-2xl
      "
  >
    <ReactMarquee reverse pauseOnHover duration={40000}>
      <div className="mr-10">• Python 3.10.5 Released</div>
      <div className="mr-10">• Python 3.10.5 Released</div>
      <div className="mr-10">• Python 3.10.5 Released</div>
      <div className="mr-10">• Python 3.10.5 Released</div>
      <div className="mr-10">• Python 3.10.5 Released</div>
      <div className="mr-10">• Python 3.10.5 Released</div>
    </ReactMarquee>
  </div>
);
