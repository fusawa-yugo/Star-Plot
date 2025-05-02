import Header from "@/components/Header";
import ImageUploadField from "@/components/ImageUploadField";
import Link from "next/link";

const Main = () => {
  return (
    <div>
      <Header />
      <ImageUploadField/>
      {/* テスト用 */}
      <div>
        <Link href="/skeletal-points">
          <button>skeletal points</button>
        </Link>
      </div>
    </div>
  )
}

export default Main;
