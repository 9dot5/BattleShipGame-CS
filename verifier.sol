// This file is MIT Licensed.
//
// Copyright 2017 Christian Reitwiessner
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
pragma solidity ^0.8.0;
library Pairing {
    struct G1Point {
        uint X;
        uint Y;
    }
    // Encoding of field elements is: X[0] * z + X[1]
    struct G2Point {
        uint[2] X;
        uint[2] Y;
    }
    /// @return the generator of G1
    function P1() pure internal returns (G1Point memory) {
        return G1Point(1, 2);
    }
    /// @return the generator of G2
    function P2() pure internal returns (G2Point memory) {
        return G2Point(
            [10857046999023057135944570762232829481370756359578518086990519993285655852781,
             11559732032986387107991004021392285783925812861821192530917403151452391805634],
            [8495653923123431417604973247489272438418190587263600148770280649306958101930,
             4082367875863433681332203403145435568316851327593401208105741076214120093531]
        );
    }
    /// @return the negation of p, i.e. p.addition(p.negate()) should be zero.
    function negate(G1Point memory p) pure internal returns (G1Point memory) {
        // The prime q in the base field F_q for G1
        uint q = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
        if (p.X == 0 && p.Y == 0)
            return G1Point(0, 0);
        return G1Point(p.X, q - (p.Y % q));
    }
    /// @return r the sum of two points of G1
    function addition(G1Point memory p1, G1Point memory p2) internal view returns (G1Point memory r) {
        uint[4] memory input;
        input[0] = p1.X;
        input[1] = p1.Y;
        input[2] = p2.X;
        input[3] = p2.Y;
        bool success;
        assembly {
            success := staticcall(sub(gas(), 2000), 6, input, 0xc0, r, 0x60)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success);
    }


    /// @return r the product of a point on G1 and a scalar, i.e.
    /// p == p.scalar_mul(1) and p.addition(p) == p.scalar_mul(2) for all points p.
    function scalar_mul(G1Point memory p, uint s) internal view returns (G1Point memory r) {
        uint[3] memory input;
        input[0] = p.X;
        input[1] = p.Y;
        input[2] = s;
        bool success;
        assembly {
            success := staticcall(sub(gas(), 2000), 7, input, 0x80, r, 0x60)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require (success);
    }
    /// @return the result of computing the pairing check
    /// e(p1[0], p2[0]) *  .... * e(p1[n], p2[n]) == 1
    /// For example pairing([P1(), P1().negate()], [P2(), P2()]) should
    /// return true.
    function pairing(G1Point[] memory p1, G2Point[] memory p2) internal view returns (bool) {
        require(p1.length == p2.length);
        uint elements = p1.length;
        uint inputSize = elements * 6;
        uint[] memory input = new uint[](inputSize);
        for (uint i = 0; i < elements; i++)
        {
            input[i * 6 + 0] = p1[i].X;
            input[i * 6 + 1] = p1[i].Y;
            input[i * 6 + 2] = p2[i].X[1];
            input[i * 6 + 3] = p2[i].X[0];
            input[i * 6 + 4] = p2[i].Y[1];
            input[i * 6 + 5] = p2[i].Y[0];
        }
        uint[1] memory out;
        bool success;
        assembly {
            success := staticcall(sub(gas(), 2000), 8, add(input, 0x20), mul(inputSize, 0x20), out, 0x20)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success);
        return out[0] != 0;
    }
    /// Convenience method for a pairing check for two pairs.
    function pairingProd2(G1Point memory a1, G2Point memory a2, G1Point memory b1, G2Point memory b2) internal view returns (bool) {
        G1Point[] memory p1 = new G1Point[](2);
        G2Point[] memory p2 = new G2Point[](2);
        p1[0] = a1;
        p1[1] = b1;
        p2[0] = a2;
        p2[1] = b2;
        return pairing(p1, p2);
    }
    /// Convenience method for a pairing check for three pairs.
    function pairingProd3(
            G1Point memory a1, G2Point memory a2,
            G1Point memory b1, G2Point memory b2,
            G1Point memory c1, G2Point memory c2
    ) internal view returns (bool) {
        G1Point[] memory p1 = new G1Point[](3);
        G2Point[] memory p2 = new G2Point[](3);
        p1[0] = a1;
        p1[1] = b1;
        p1[2] = c1;
        p2[0] = a2;
        p2[1] = b2;
        p2[2] = c2;
        return pairing(p1, p2);
    }
    /// Convenience method for a pairing check for four pairs.
    function pairingProd4(
            G1Point memory a1, G2Point memory a2,
            G1Point memory b1, G2Point memory b2,
            G1Point memory c1, G2Point memory c2,
            G1Point memory d1, G2Point memory d2
    ) internal view returns (bool) {
        G1Point[] memory p1 = new G1Point[](4);
        G2Point[] memory p2 = new G2Point[](4);
        p1[0] = a1;
        p1[1] = b1;
        p1[2] = c1;
        p1[3] = d1;
        p2[0] = a2;
        p2[1] = b2;
        p2[2] = c2;
        p2[3] = d2;
        return pairing(p1, p2);
    }
}

contract Verifier {
    using Pairing for *;
    struct VerifyingKey {
        Pairing.G1Point alpha;
        Pairing.G2Point beta;
        Pairing.G2Point gamma;
        Pairing.G2Point delta;
        Pairing.G1Point[] gamma_abc;
    }
    struct Proof {
        Pairing.G1Point a;
        Pairing.G2Point b;
        Pairing.G1Point c;
    }
    function verifyingKey() pure internal returns (VerifyingKey memory vk) {
        vk.alpha = Pairing.G1Point(uint256(0x066f049a2f21f213d8b5cae891541e5042afc5d6be7eed90da1bb1fff31df588), uint256(0x23f650ffb52dce16d44cf65c90d33dd53813326387e6d8bc9c999ba8892d1eea));
        vk.beta = Pairing.G2Point([uint256(0x0f5e98072f3cb4fc47375364ea24cb89cc0270b5407b09c069f984133df0ff64), uint256(0x2d7b2af508a21ffd5554082dc9efd04ed33456c3ea9c7fdde4799d6a28ad0602)], [uint256(0x18c5a837a5cd37ef6a4d808e58b427650204e98a92198be6c0b5d7d7b91776d4), uint256(0x07274942c5fce310d56b98324180528588ea6871afdb64b5471728edd31f94f8)]);
        vk.gamma = Pairing.G2Point([uint256(0x05d86d0cd4f642b90792f53abd425bc4deb413ed1fd0a063b6d5c2d1db905559), uint256(0x19e90cc9fcf9a670af4f98497e6a7f838c930ecca9b7c4759d69b2ab35ddb1af)], [uint256(0x0e34d5dbc925cf56214e053523337855a1cff1d1984b3cd19902f8f9f9087c66), uint256(0x2406bdc9a338d5818be511195b9d75e06c3cc6475280b8116d6e66da0e01bc5a)]);
        vk.delta = Pairing.G2Point([uint256(0x17a1861340596370cfa2c7c05d52428f6f061a905988c1e27264d1e890e252ff), uint256(0x0db6e5c3877a61c586c0535d366793f2fa7aca25a5b0b9ce906efb154f8bcda1)], [uint256(0x1bab3a6846b5dd42965dbd6590b01b391d056d1f279967dd4eae6177c658ffb0), uint256(0x16382cca0e959e81f824c54c25dd91d820856cbd18808527395a59a5cbd7c75b)]);
        vk.gamma_abc = new Pairing.G1Point[](109);
        vk.gamma_abc[0] = Pairing.G1Point(uint256(0x1c4299f3c220d275edd97c9df63c12f9930dd93ed9200e49e132ee31417e1b31), uint256(0x185db4772c8862ebc2aefa7a46012f2779781d3225bd87cf62ded90f4f0d2920));
        vk.gamma_abc[1] = Pairing.G1Point(uint256(0x279eb129f5a112fef1f825252491272b183f7adceadd058648b817ceb93d3edf), uint256(0x1b45b7bce43e772683cfdd365658492e081a6d8c56c8f872709ac8e4309ba910));
        vk.gamma_abc[2] = Pairing.G1Point(uint256(0x261fd884848a39aaaa737b4d933497f37effd345c378f2747aef4c806234a73e), uint256(0x045c62595b42578d9f1197d229dcde5e05138e23daf6d9c93ac02506b6c98872));
        vk.gamma_abc[3] = Pairing.G1Point(uint256(0x0fc3908ff2e42e3b469835f597186c67d84c9b7241e3317a0e846c53d9f6c9d2), uint256(0x27693e22bea5ab81dd29158f952cbd4fc497af3f4ab353a7c9399663b5079268));
        vk.gamma_abc[4] = Pairing.G1Point(uint256(0x0fdc14ae103a53d86c65532798ec34a562656342802171189d2129ef91bcd1fe), uint256(0x2392e14c81445a2ace91e3e442b39e44e9669bd59fc0b6b6b9d6e7f14145adeb));
        vk.gamma_abc[5] = Pairing.G1Point(uint256(0x133230b582a4b5d97cf87fa9e3201524de05af88c500758381175bcc78aa9dfb), uint256(0x1180f8aa5bf55754d8cd966efde183c463e64cb84b099c3a3c6475cad223c566));
        vk.gamma_abc[6] = Pairing.G1Point(uint256(0x170a5602f77014bd8af9e985d83811cb194ac4c436db16782182430952436f24), uint256(0x1f36fecbac46eb662cb1f960aea4bdc0864fbb2b4c54d7177a5feb22f58b1b84));
        vk.gamma_abc[7] = Pairing.G1Point(uint256(0x1bc23e583c28126bae9a9a8ad92f55fa5a31597c529177439bcded91a666d247), uint256(0x18eaefa932f5effe8d19ab003a418eddc95a8dfdaf109f85cce7df9d6fd35d89));
        vk.gamma_abc[8] = Pairing.G1Point(uint256(0x0acb47596a7c6b99a1980b0533825790207fa635622997b6cb778095e23c815a), uint256(0x1516ce71f4fc3af6ed9c1c5529c9b43637edfcafb76c0d511d0af8d9a48594cd));
        vk.gamma_abc[9] = Pairing.G1Point(uint256(0x0f78eba1cd20d2ebea1b00cec24033b9aa42902f3d634399c5ce92b469cd2def), uint256(0x276da7913e29d9bebda4955f0b0a09814459949859739dc4d3909ae42c531eeb));
        vk.gamma_abc[10] = Pairing.G1Point(uint256(0x2d367bcd16d2b8ca2bd85efece0ac1fbab0436ed5eaacc6bb7935667bd006598), uint256(0x13481cd2c6ffb9c9efcefb6ab444c1ec06c2e53ac60ba3966f6066d9629c73d7));
        vk.gamma_abc[11] = Pairing.G1Point(uint256(0x26930b02d867c821236f5d100c0895a7f4af3d66f7912bef73598ed224ebd459), uint256(0x1ece72eae018f59a20ab1914fdaf880e83f29473bdedb7da954693dd89f95a94));
        vk.gamma_abc[12] = Pairing.G1Point(uint256(0x068b4e1faa01565e451280dbcfa648c7e35ab50e3cefc4759fbdbc8a3b784b1a), uint256(0x047cf8a598b332adefc2796cb8818316d8bea8e6c9aefe58d5f4b6796da0f372));
        vk.gamma_abc[13] = Pairing.G1Point(uint256(0x25cee41492679e595caed801166b378f82c65e6c3900c50458728277c2de2c1e), uint256(0x06247edff500810a4287dbb7feffe0770199d87437a01f4e95552124328715e3));
        vk.gamma_abc[14] = Pairing.G1Point(uint256(0x010a0364286c4631db86c6e5cda5a92e63a83938c1c76d8376c84dcf29bedcae), uint256(0x0c425df6d1ff55b8f3cfa574be89ecd008ebb16364ed9a4e73c76d8eb41eb813));
        vk.gamma_abc[15] = Pairing.G1Point(uint256(0x2b5c4c9270fb9070916fc32f0ed30c1dc34ff9208f31834ad6e9143a33773517), uint256(0x1ad784f2c7a790c644b338f90bd603d2c42cabd98e971e022fc8081e25d162c0));
        vk.gamma_abc[16] = Pairing.G1Point(uint256(0x00d161168f93b3c636dbd8109b55362bd5050a5d4f1138eddb8aa2af459666f8), uint256(0x1041bce79aa0e7aad5aa1e17216efddabf84599191e276e435679bcabc07f1c9));
        vk.gamma_abc[17] = Pairing.G1Point(uint256(0x29f7536d70a9131ccb8101ae9563188027cad00a03fd779ad653e8986da6d939), uint256(0x2aec90d1a738e076717c9f2aecddd14b8e6eaf7a9bfca71fc17ac64cc52da481));
        vk.gamma_abc[18] = Pairing.G1Point(uint256(0x0b8e17b3673c32f7c7be6843d540edbc072adc53bfc1226eb72bfac24a836e4f), uint256(0x01700bcf353c473845fd6846ff561cb208da8e0d99150d5a19e44b20e4219f3c));
        vk.gamma_abc[19] = Pairing.G1Point(uint256(0x2f90c4f4fc6ca7aad0e752ea0de471bbb79e43a019f1c1908f9154c349128f0e), uint256(0x2da8ef60f54a7f961b47a15620614d2ade17c8352310b703912337f3e0554e66));
        vk.gamma_abc[20] = Pairing.G1Point(uint256(0x07c171b63ef74b6ad6ed584c73630bde3244d21bd4f708874be9048ba86f5f81), uint256(0x0346f2a72096bf00469af549fa38dce8b711ab428e3261773b13930b63ac9e7c));
        vk.gamma_abc[21] = Pairing.G1Point(uint256(0x278aaa6f9676833bde9460d54274665b4b47721465b1eb3ee7c3cd310e1280ca), uint256(0x2cee1ddced6f0a7157fb829a0ec4cb65e8d012b18a73e0d5ce17ed950475d278));
        vk.gamma_abc[22] = Pairing.G1Point(uint256(0x057b282dcfa8a0b024671aebb5aa6bb7e2fd0d018f078f4011a60280b93688e2), uint256(0x1f803ef77a064af5feebdbed04e0787ee1efc9cd879342ab89a2112eb80c564b));
        vk.gamma_abc[23] = Pairing.G1Point(uint256(0x1695927eab4201eb4dcc90b442131c03e3a5186e7e0ace24f06c6e16e0244983), uint256(0x104d408dab746befb62241f6a9bae88ef166197cacec02229fbe5d1c29a7a178));
        vk.gamma_abc[24] = Pairing.G1Point(uint256(0x0bf01ade7b002affe411e871f3e03dfba2292482609733608a5b519ac852859b), uint256(0x030a9de0792cd68a2b2d9cdf3d824591f32ca8d9aa84056a6d7ddb91b67e44eb));
        vk.gamma_abc[25] = Pairing.G1Point(uint256(0x0b8c6c8fc6dbea2a6458b0fa3ab35397638b7236b35d657ebf3b47ae28a3a045), uint256(0x08918d4fbb9663d7e71cc636ebe7cc0de56b6159c5a6b1d648e428295951de17));
        vk.gamma_abc[26] = Pairing.G1Point(uint256(0x1349abf413368270e1daab6a183a0e9d409635ad42e77769358a086cc509aacc), uint256(0x0744c27cd3061e7e832cbfddbb159e98a87d1499d56714e57a779fc3c57184fc));
        vk.gamma_abc[27] = Pairing.G1Point(uint256(0x0380117372df3914eb3f79ae500ba9010e22f2c4f82f3a9d395a1144c13e1f3c), uint256(0x2e09399027e1201f201494a674792af8eb1b23dc8d7d1553c5f5ec4db095ded9));
        vk.gamma_abc[28] = Pairing.G1Point(uint256(0x1e9c3feb0ed20b1607a1eedc5d9fdb9e4fd7faff7d135ab5e9626d34799c618c), uint256(0x2a62b7b4324d6cde44eafe643548738e91b41157c5da3d7aab80142c1517a254));
        vk.gamma_abc[29] = Pairing.G1Point(uint256(0x236c86b22f0d75b64ca5d25299bdbda063410df554676f1a6a6fe0b1987f0d0e), uint256(0x2821e883055cd0bc7f27f5c52a57e4e5274018a2360377cfdf45ffa1a40bb663));
        vk.gamma_abc[30] = Pairing.G1Point(uint256(0x1d80cc970668095aab76e032c329478b5f2c1ef376aeafd6bf776a3e843a7f06), uint256(0x2e82b9642ca9f7be2e00ce48c61876d2e04bb1d2be2b176b667d61dcc94d079d));
        vk.gamma_abc[31] = Pairing.G1Point(uint256(0x28452a9b9f6a4a7887b0b9167d6ddfbee5dade3127ce6e68cfa57f47ef761c65), uint256(0x21aceef89ab864e1720b1ebdda32876ef2bcddc38d096585a64c8c349b8203ad));
        vk.gamma_abc[32] = Pairing.G1Point(uint256(0x28b7d630502ca7f0ef2fd62f02b82d9862c5a57e7d28bc865359b5e4b4fd6ebd), uint256(0x1a0a352f884a417ca8c271f0d3275cf9a7bdd43aa6390ef675c244de9348aa67));
        vk.gamma_abc[33] = Pairing.G1Point(uint256(0x136785d09e9f3ca15bfd2c8d442dc68ca629a0ce845bfedc2b9c5ad84d57d7c0), uint256(0x0201bcfddbcb7288506a22115ac687fb9fd29f621091179e7a4be2f4df2fe71c));
        vk.gamma_abc[34] = Pairing.G1Point(uint256(0x2a0115b6379833cd075b30379d48da5424375ad565163bd6a3ab9cc50e383793), uint256(0x253ec2fe39b33d84d22a6917d00cbb8ea5e02ba4ff5905eba04459625931176b));
        vk.gamma_abc[35] = Pairing.G1Point(uint256(0x2c0ed2768ee19920f25424edbb91fc4ee2bddddf5f7a5e282e600b3b6d4ce15a), uint256(0x14d74ad7e5cc489cfbc87693548dc074596b42abb8b1bb1c493d24cdbb489a02));
        vk.gamma_abc[36] = Pairing.G1Point(uint256(0x2b04b87b4617859fc8796e93fe0e7a33424ef2d77e9f65406fc5cb440e761194), uint256(0x2dccf0bf634fa4dc7b466f07e161832aa7b1ed3b838cc52c9c7e93b024d62b3a));
        vk.gamma_abc[37] = Pairing.G1Point(uint256(0x21500321212cca5c4d1e42a744bb04ab78cce72f49858fcc7848617d22ce3cc2), uint256(0x2f4b8eacd445253531b2cb28f8a643100d4216ea6f1a42910ca0b0aec4862005));
        vk.gamma_abc[38] = Pairing.G1Point(uint256(0x21dc615adf6f3e6f312fb12aaa0ffa95aff9ffcc161222418a3c81082358c210), uint256(0x1b472dcc5c8c059a117cc4cbdf32eb8897302f12b167e2c9cb70fd7d26c1eb43));
        vk.gamma_abc[39] = Pairing.G1Point(uint256(0x0b5f026eadc5598a9a11d7379af2ba1b9f67793e321741a09ebbd29243e630b2), uint256(0x16934f9a2fe20365b40e04df9e635a8abccd0b9287811dd9ddd3a48b08f4e317));
        vk.gamma_abc[40] = Pairing.G1Point(uint256(0x2d4471bab0f372d96062ef267a13d1d6c5e294de0530afb79d8b8c84c779155e), uint256(0x24f4b05a703f04cccd02d89708080534dbe6eb4921bd5b820dff253cfa9f2929));
        vk.gamma_abc[41] = Pairing.G1Point(uint256(0x08e52416d1acf3c4316a281dba3467ee608cab265ceaeb47430e89f229fb1f76), uint256(0x0a9f59e0e58d9aaf87666671cd3da638f3ff1f26cfeb97158743baa69a89545c));
        vk.gamma_abc[42] = Pairing.G1Point(uint256(0x2a02df4e7da5ddaaf6159b8a7300def2f9870d51a296dae0a968dea49a27a039), uint256(0x0cae889a821c2be5a95fae2e4c729d5abd8819f8e6c0b584f15a745ac68fe4e8));
        vk.gamma_abc[43] = Pairing.G1Point(uint256(0x1a5b99ccfa60922d8ab960cf2477e281fe12fb05f9bb7510f87c04e4403df5fc), uint256(0x007867b5bb1eca95b47dd852ea2d8e804dd1e4a0bb6a0e029a08d8e2a3b8ba68));
        vk.gamma_abc[44] = Pairing.G1Point(uint256(0x078242e937319b31652c3c18d22746c6427730ff3437256b572ba911ece36eae), uint256(0x2860a9fa77f51975f0ca04ee1aea7305582e47b0458553e6a53e633698df6566));
        vk.gamma_abc[45] = Pairing.G1Point(uint256(0x020741810e37f11f6a80f22f99d3f61f94ef20c97eeba42cbc7a7b755141e437), uint256(0x03862bdac3beb62d626b0673faed1bc4ceda55bb090624ae03408c65358e7865));
        vk.gamma_abc[46] = Pairing.G1Point(uint256(0x2d715b64a607b4c24ecd666a602bca5386a1de5fde015292dd4eac40907ffaf9), uint256(0x27f2c30fb71607a7c24181ccc4ab0c5cb784e28700e4d3adcaa4706639b0aa25));
        vk.gamma_abc[47] = Pairing.G1Point(uint256(0x2a7e14f52b5d23cab6260467aac23e83b361a2b91e85174bf65f401300184e88), uint256(0x2cbb470c21e7a653bbc7023488c99f4584d5e952af69c81c8bba4eb1d57e303e));
        vk.gamma_abc[48] = Pairing.G1Point(uint256(0x08c6acdfdd0bc6d197c17d8fff3f4e1b507dc6facb659fa7cfbfdef1c3c28490), uint256(0x0cf2d23f8d51807eaed97df7daffb3b99fb4d093755b402daf1f8fe12b822eae));
        vk.gamma_abc[49] = Pairing.G1Point(uint256(0x1b40232b0023ceaecdcb890ce7199b9460feb505722c6085e39d6c663bd8b2b2), uint256(0x12e10029b9aa2e0ddb4c5bc0a32f08e5f797ddd1e3738123baba0694e8506afd));
        vk.gamma_abc[50] = Pairing.G1Point(uint256(0x0234bf87533a50bd0cb1f5d1e64f273806ea9509894c139d42f5262396786105), uint256(0x11be6273f2bd389064ce2652d7eef21a96e5fff5ed4ad1edc94aae0fde1b7230));
        vk.gamma_abc[51] = Pairing.G1Point(uint256(0x125142f88504f3fefec1c8d9faff156bae8be9b84c809e57235ff910e6594de9), uint256(0x2f03492ffe456982ed91351e6d69371e977d7e1073243a0adb1e02c3a255c3f4));
        vk.gamma_abc[52] = Pairing.G1Point(uint256(0x19e5f15a093f64a1acb4a17d16b4561349d3e8f9e08f95c217cf85e4996d1684), uint256(0x10dcc7a8ca019a9f15d71f2109e9289925f5d441b2496be1baac2007a67a7212));
        vk.gamma_abc[53] = Pairing.G1Point(uint256(0x143f1d4ce08b253f7be0a3d84fe13ae157588ef092916d29794220f240d78767), uint256(0x08a095ebde4c8486a261eb484483bc8deaaa997b38a141e2024f4532e04dd59e));
        vk.gamma_abc[54] = Pairing.G1Point(uint256(0x1c39b2075e9ae755a83535e52bb795a49e52eb6a437dca612fba11171621c76e), uint256(0x16849d2288e30b8e02c9dd654053156b792c482d3c05e582cb5550349328b528));
        vk.gamma_abc[55] = Pairing.G1Point(uint256(0x0fc2b6602c9a67b2866b2ea6b74085f062a69f6bc38bf8ae3a0f00f27f9f9832), uint256(0x18720d9b303260c8a592270591829c41e2fe8a77521b1400adfb676fbb971c12));
        vk.gamma_abc[56] = Pairing.G1Point(uint256(0x1b5d5dbd607a22bce8f13cd4413b606079fdccf4f11168bdea745cbf1dd86985), uint256(0x1e940af3c0527b54db678d877c85cac07bd0f42ba7b26c1e1ccfebbf2a879e0e));
        vk.gamma_abc[57] = Pairing.G1Point(uint256(0x0926d376725e93ffc65ab3892525d6c14b2cd8e2557866eeb001bb2e0d9a0d90), uint256(0x304f9e2034b2fe78545f99a0b1ed4e104e7d93a446cb952232bcb67d5339c3b0));
        vk.gamma_abc[58] = Pairing.G1Point(uint256(0x02c91480d3664d952c7015b79c288a773fd3c0e466cb9a311892396c1f7235fb), uint256(0x24ce2bc6fe306fcdff8cafb008ef8e0a1252796b1c0f129e8ca8b42912ae4bc2));
        vk.gamma_abc[59] = Pairing.G1Point(uint256(0x12b95100fd3671a6ca66f9de2a2ac49e5fcfb216b28c913d3283fca6a0244bce), uint256(0x23b72257816842fba1b01b6617a18c71aa06ed3c964433ef947dc893d7019ee4));
        vk.gamma_abc[60] = Pairing.G1Point(uint256(0x25f3bd40efe959d124fd3de9305f2bc81e486ec70d78807a3a8b5dff167132c7), uint256(0x0af639240aeb9824453c212656d899cfdb1776e618f8d746ac5fed10825ad9fe));
        vk.gamma_abc[61] = Pairing.G1Point(uint256(0x223b5424ce3cc6fffb31d3adf11dc67e33d28a99f121f1f3f176b0f52e517b3f), uint256(0x0056ca677368baed07985dbe8cf26852d8f1bffc0a74508e5a69655d1e711ed8));
        vk.gamma_abc[62] = Pairing.G1Point(uint256(0x08fd12d5f6143ca67aaa3a6609d043d158d3da9b460b1d59006b5faf2d6a944e), uint256(0x0d9a68d531f3dffc2febf050f146ad665bbda48b29d5cda1854806c10d4b9092));
        vk.gamma_abc[63] = Pairing.G1Point(uint256(0x302c6acff19473c8684f75a1f6be38b721eb18448f5859e031bc72aa0dbf8a00), uint256(0x2d3a3684d2fb67db8de562ed17d5ed51a3f541941aa3b27e23dce5a5a4df0bdb));
        vk.gamma_abc[64] = Pairing.G1Point(uint256(0x10ac017b9872838e3ef745f7efad59efb535bf7f29cdca6e204997eb0122302c), uint256(0x2f495550c1b7339b3370b5486dfe14b2e56df930db3d7371e9ac757f64aa3e5a));
        vk.gamma_abc[65] = Pairing.G1Point(uint256(0x03e81b3b876880a1c5a7fe252a26d652990eb52258ebbd714ece0e180fd45612), uint256(0x1cd22f36592090c8d7ee8dd79d371a483371f95fe1f7fa44a65e10e86392f5ed));
        vk.gamma_abc[66] = Pairing.G1Point(uint256(0x06473a91e4fd8be01283647ba13b3bd0e1fd39ee9c35642dcaeaa9f64afe0694), uint256(0x067a10975fbbeb9d17aa637da36deb3f09e57701db8d67b681ac5be405213913));
        vk.gamma_abc[67] = Pairing.G1Point(uint256(0x12846a46871e7237e657dfe1cbe2731ece3cfc5c80e497b2883eb549ad4ba889), uint256(0x0b808d7d2718ecf3b8101c95224d199f4fac7ba5c3db9af6884d2f8f51d03e28));
        vk.gamma_abc[68] = Pairing.G1Point(uint256(0x150ddf4f6e2d255fac14da37337396a431389dce5ca55363ab4b8c9d38a2789e), uint256(0x04ba5eaa102c73d2a7c25f0165d23f46b0f623bf75535a2286badc2a0142e495));
        vk.gamma_abc[69] = Pairing.G1Point(uint256(0x2d11cf88c3bbf5531f4f51858891795116734795614bccaacdc1c799d339e89e), uint256(0x070f574f7e6dbd392629418cc4ebbbca52c914235454a82d3e29af0a5d623b2b));
        vk.gamma_abc[70] = Pairing.G1Point(uint256(0x199dea9065d5d748018271a848a3e278d42af0590c2caa555a6025694311cae4), uint256(0x243771c2dd1cad00440e0e498b75c0b608128526ec1db19ee0248d69bc12a458));
        vk.gamma_abc[71] = Pairing.G1Point(uint256(0x30624b739d2ce2922f776ed8277f6b57942e390c478ee8976d52bb5d1d74b356), uint256(0x14ed85c83a2eda4f4c61492ac0079e89730dc90c5d3b4307a07477bace35bafc));
        vk.gamma_abc[72] = Pairing.G1Point(uint256(0x2cccc2167a6f4a213cfd3a02a67a7f472865dec37060b08888b4dcc8d4d2358a), uint256(0x020bb5172d66c0c00bbea8bce90e2c2a5b983680e1dcb0047ac487bd7324aca7));
        vk.gamma_abc[73] = Pairing.G1Point(uint256(0x1294bf157ee233c3ffaf30f8e78fd8baec92a9c21eeb7bbc5282203fd97241c4), uint256(0x0311ccd03c221748dd060996c262c74f9c933760db2cbfa224464f408e717d9c));
        vk.gamma_abc[74] = Pairing.G1Point(uint256(0x2c1db89fe98457f7bb310d5c62e2334af818ab6050fdba253acc779b29d6cdcd), uint256(0x199c19a3b1c93f38ca716aaedea41811c35ca7031455bb2bfb789fb9665e9816));
        vk.gamma_abc[75] = Pairing.G1Point(uint256(0x3037d4523703a0fcf4a76ef881aff4bebc419e6387fc96f98cfa220ba90eef96), uint256(0x2eaab72e73494ff16d3bce86e0ea07399b8f6453b5783d1d70dd4d5c1a964175));
        vk.gamma_abc[76] = Pairing.G1Point(uint256(0x113a531ced5a0dfe78883f5dfda8c43c470e3ecec7eae09ca5fb06f714463522), uint256(0x20e131ff1232924606e53802d880e078a17e1142c95d29e065d610da48367557));
        vk.gamma_abc[77] = Pairing.G1Point(uint256(0x28ccacf9fa0a7b0a8a70e17434af0c85c7e0bceb975755cb8f94b5bded218bc5), uint256(0x1cbe9b6b00ae5377003079b1c5f99f345d7b69b106e44a8f59e81ef064e22e38));
        vk.gamma_abc[78] = Pairing.G1Point(uint256(0x1c6467a1eb30eb73f607aa7a967a4a619c01628a0f6d460f5243c8e9008ee66a), uint256(0x23d54c5c56fbf26a0905087cd5714de3c4e0edc5ed9387ce8a8bd756a128a5a8));
        vk.gamma_abc[79] = Pairing.G1Point(uint256(0x10b937a800051423fb2374a61e79bf4dd76c966548211bbefd3a739f05b06945), uint256(0x0642b240b9d57edb8b13c9f3bf185af9f1fe7b547f39aa914bba83c0649b8b66));
        vk.gamma_abc[80] = Pairing.G1Point(uint256(0x2f72f601d23ce43584bd7ddb6464c5980efe32f785eec0644b4eb4a136710863), uint256(0x0ce50d61ccf4b110158a650eb3025538d19acd12ee8a5f870159de38529bf4fc));
        vk.gamma_abc[81] = Pairing.G1Point(uint256(0x02298d3035252f46dd7f8aeb0216efb00ebb0cdd2bfb1cb4a894cb403c608422), uint256(0x2f474b35b5f6e21f434963ff4b13f4fe7d3b742ca4f026d5f6e1fddd0dbe6613));
        vk.gamma_abc[82] = Pairing.G1Point(uint256(0x1fb8b32d9a3ca4043c352a8188c2d412494c6c0f444673d20fc950b0a937e94b), uint256(0x102ab4fee31d2f8b0f4748d838e2e38c3afbff8e42848c404c0f38db6c4c4005));
        vk.gamma_abc[83] = Pairing.G1Point(uint256(0x09cf5690db6bb2c6f0779d93f45401cf6552c733e09b93bec986714789d15d42), uint256(0x2f7959618f7ffc96b4bd96d7f9f5ce2d4849aa045887dfcda2ea97a42419f85b));
        vk.gamma_abc[84] = Pairing.G1Point(uint256(0x2e33df4fc6a49ff19fca5f55d3f8071311222809058b8187fc2d265bddb44721), uint256(0x1cc3f62441ae313d6032e834e2b0d07139dd9e967971169ba727946ebf82ecb3));
        vk.gamma_abc[85] = Pairing.G1Point(uint256(0x2e5ca6d062bb4f242ce261006e496763cf7735db08dfcaba0e77e960d092fa32), uint256(0x2291ea74f3e2342a9581a15dbe384aaee0f1e6678a859ed5185d97dcec7801ae));
        vk.gamma_abc[86] = Pairing.G1Point(uint256(0x22b90104d31ced9d1df6dfca88aad78595bbdaea20f2166dcf00f01f966206c7), uint256(0x29155919e9ba3fe3abfe845086cd6d80a6d7dcd9569840f55165e67761c63fa2));
        vk.gamma_abc[87] = Pairing.G1Point(uint256(0x1847c19bd765874391d66ddf8a358050a2a98473810d7e9d0a12b398a5a84ef1), uint256(0x08d7d408a06d319db948d43e24ef3c860e28bc2ff137b9d60d41e1d477689fec));
        vk.gamma_abc[88] = Pairing.G1Point(uint256(0x1021aec9aa4499d800ce7e2b4cf86e164bda6ec2a86f22975aebcd4dfcd847e3), uint256(0x02149bf7618e14a89618b1bb522e665ee264ca137c1ee506bf23b53e4d741798));
        vk.gamma_abc[89] = Pairing.G1Point(uint256(0x1f5507a228771256764f60f7cf50bb52c702b647e91b6fcb6a1097f1e2ece1e5), uint256(0x01b3ee0a78f26e5e6897a35109059e0fb4c61d8ac9d60b39ccc37ceddbf6b448));
        vk.gamma_abc[90] = Pairing.G1Point(uint256(0x1eeb12e709e4b648f7a1aa6457fb7bdc76df88aca3111a4ded5cdc5a25833b48), uint256(0x28eae36b8bb81efea48d021f0900f032d2fb6695defd38a06b935d3f810d29b3));
        vk.gamma_abc[91] = Pairing.G1Point(uint256(0x0ce018bb4a65022b47ab9694b9bf82822cd9838d16b25724f3b0fa76071b3811), uint256(0x2cb6b445da05603838cfea2528ca76adde77e96690a5bd4227ea715af706d039));
        vk.gamma_abc[92] = Pairing.G1Point(uint256(0x19f39dfc7f4823700d85a2e30e5dbbe5af35114a71597b34a5be153e6cfa2138), uint256(0x14bc08907010e8c5a18f70018f24648873a54f5eeae19f31a2f0cc66f77bb70b));
        vk.gamma_abc[93] = Pairing.G1Point(uint256(0x1ed98b317750a185028f80e06ee523ab347927eeda9c82d3a236c97d44a2de40), uint256(0x01658a85b541d6050192030ecf191f60950381b971c9709dd45bd3add82427ec));
        vk.gamma_abc[94] = Pairing.G1Point(uint256(0x17a627569152b26789b6042bd8054a1d559b06808a7987faf3a4f19d6b3c0fc0), uint256(0x0d482d794402d29e663b38379b710baf72c08bc9d293d058ae1227ab3978b4f8));
        vk.gamma_abc[95] = Pairing.G1Point(uint256(0x2bb52d3f718af028055391e153a11d9c8fc4af2af81e3403a153eb99b3c46a5c), uint256(0x1149ace6c120a5cd85b8f38457a77e92896a5149bfc76dd22b7fd67c68df35e5));
        vk.gamma_abc[96] = Pairing.G1Point(uint256(0x05a02fe20a24da1686d4283c0a2865757798760205e484e617072110457fe8b2), uint256(0x2b9e6a153de2406046dc01d76090f5671e35e857acff4d2dcd3a9d670d8ff4f9));
        vk.gamma_abc[97] = Pairing.G1Point(uint256(0x1261f3c40c1605b8820de29689864895fccc111c5e1b3105aa60d5c543800e5e), uint256(0x300d8ed87faac59fa7f3cff5e905976eef964eef44b8a9ee7e59a6bd6ae54f3a));
        vk.gamma_abc[98] = Pairing.G1Point(uint256(0x2fa3120afdf9b8dc5b6f0744ea0e34174c53df7b5dc18fc3ccf2e39acb7060ba), uint256(0x0b9c8567a9e436643116417100f6b14919793d2fca2d6e246670a87738b9f455));
        vk.gamma_abc[99] = Pairing.G1Point(uint256(0x2e9237935fbc19c580d90fe134d8f727d7ae49898817f80b4f0951b8917e5d6d), uint256(0x01bb7fe6248672fdf0ca7c7c4e9fafe0c3000eb1c79b4a91d0669b2335575a9b));
        vk.gamma_abc[100] = Pairing.G1Point(uint256(0x191dd41338fe422896748f7f2cf6ff3bc2c1ccdbd82c504696ba25332d92c426), uint256(0x19e2edec4f50530710c78f0b23173c115ef380228fb780c59e78df9e6f7135d8));
        vk.gamma_abc[101] = Pairing.G1Point(uint256(0x17249b82474bfa6d6d1dbd05a9a563fb28be49f1495cd145ec9902679e980076), uint256(0x0b8332427084aadff2f80fab4f526ade007c9044a665b6d37eefce6a559b39aa));
        vk.gamma_abc[102] = Pairing.G1Point(uint256(0x2733358c8a643c59070bfa2eb6edd3fbdafd1406ddddf3b12c15c4b8f4f691a1), uint256(0x0e90ec4da49ddd479ec27460549e7e48c0d184764420de2755277d7c7928f2b6));
        vk.gamma_abc[103] = Pairing.G1Point(uint256(0x2ee1cc59302e39d965c8299c48bb0e4ad799f702bec0d9055d7473bdb63f4c72), uint256(0x191002a16972640e6063944b3344020b3ef2b8d9d13796a6cbc8a18679640129));
        vk.gamma_abc[104] = Pairing.G1Point(uint256(0x2ccd5afcd696bca66d26706421eff3de02e1e3eaf1f34d0d16eef85712197c8b), uint256(0x2607bbd1ff83eef7fd03dd10248106491c8252021b1157402a2c4005c4021efa));
        vk.gamma_abc[105] = Pairing.G1Point(uint256(0x19391fb923faf2d09432b87adc47c96794d80b45a4bdb0433e0e63bb4f947512), uint256(0x1f74812fe70873abf6351afd7933aeb9644250aacd24d08b3d453a31d9272ab0));
        vk.gamma_abc[106] = Pairing.G1Point(uint256(0x29e4aeb178a3e8e43a243c072595e04f4677084ff9d2f991ef8905094266e030), uint256(0x14534111e9eef3c42876f9d5bc8a6fff93090e2c6467e5b3f3ea1b04708524b2));
        vk.gamma_abc[107] = Pairing.G1Point(uint256(0x0dafdcc8180ba83878f4d3be4c0256be8e3e5f1ee4455b4a04a3785c4daedf48), uint256(0x09fe30adc08fbf197521b75aff0b746fcfb147af3c2574830e00af492f9055bd));
        vk.gamma_abc[108] = Pairing.G1Point(uint256(0x0ea13b09558f9c662fb048066afa28899067a2f4ea4196b498cac46057e56ff1), uint256(0x0ea6f23954562c27956ba80865fe257581ff362b4db099a990649f262c191263));
    }
    function verify(uint[] memory input, Proof memory proof) internal view returns (uint) {
        uint256 snark_scalar_field = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
        VerifyingKey memory vk = verifyingKey();
        require(input.length + 1 == vk.gamma_abc.length);
        // Compute the linear combination vk_x
        Pairing.G1Point memory vk_x = Pairing.G1Point(0, 0);
        for (uint i = 0; i < input.length; i++) {
            require(input[i] < snark_scalar_field);
            vk_x = Pairing.addition(vk_x, Pairing.scalar_mul(vk.gamma_abc[i + 1], input[i]));
        }
        vk_x = Pairing.addition(vk_x, vk.gamma_abc[0]);
        if(!Pairing.pairingProd4(
             proof.a, proof.b,
             Pairing.negate(vk_x), vk.gamma,
             Pairing.negate(proof.c), vk.delta,
             Pairing.negate(vk.alpha), vk.beta)) return 1;
        return 0;
    }
    function verifyTx(
            Proof memory proof, uint[108] memory input
        ) public view returns (bool r) {
        uint[] memory inputValues = new uint[](108);
        
        for(uint i = 0; i < input.length; i++){
            inputValues[i] = input[i];
        }
        if (verify(inputValues, proof) == 0) {
            return true;
        } else {
            return false;
        }
    }
}
